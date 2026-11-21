"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

from datetime import date




class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)







from .models import (
    tblIIIIbassets_authorization,
    tblIIIbprorations_schedule,
    tblCOMPANY,
    tblBRANCH,
    tblSTAFF,
    tblIIIbcoop,
    Userprofile,
    tblstandardsavingIIIB,
)

class CreateWalletPackTests(TestCase):
    def setUp(self):
        # Company and branch
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member")

        # Coop member
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, status=1, name="Coop Member")

        # Officer user profile
        self.userprofile = Userprofile.objects.create(
            email="testuser@example.com",
            status=1,
            thrift3b_officer=1,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )

        # Scheme standard
        self.scheme = "TestScheme"
        self.standard = tblstandardsavingIIIB.objects.create(
            branch=self.branch,
            description=self.scheme,
            to_month="December"
        )

        # Client with session
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKEPIN123")
    @patch("yourapp.views.savingscheme_email")
    def test_successful_creation(self, mock_email, mock_pin):
        url = reverse("create_wallet_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/mysavings_wallet_success_o.html")

        # Authorization created
        auth = tblIIIIbassets_authorization.objects.get(
            branch=self.branch,
            staff=self.coop,
            description=self.scheme,
            status="Running",
            year="2026",
            month="January"
        )
        self.assertEqual(auth.asset_authorization_code, "FAKEPIN123")

        # Schedule created
        schedule = tblIIIbprorations_schedule.objects.filter(
            branch=self.branch,
            staff=self.coop,
            scheme=self.scheme,
            account_type="Assets",
            status="Awaiting Execution"
        )
        self.assertTrue(schedule.exists())
        self.assertEqual(schedule.first().authorization_code, "FAKEPIN123")

        # Email called
        mock_email.assert_called_once()

    def test_scheme_closed(self):
        url = reverse("create_wallet_pack")
        post_data = {
            "amount": "500",
            "scheme": self.scheme,
            "year": "2026",
            "month": "December",  # matches to_month
            "coop": self.coop.id,
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "This scheme is no longer open")

    def test_non_officer_redirects_to_404(self):
        # Create a non-officer user
        non_officer = Userprofile.objects.create(
            email="noofficer@example.com",
            status=1,
            thrift3b_officer=0,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_officer.email
        session.save()

        url = reverse("create_wallet_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()  # no session set
        url = reverse("create_wallet_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/user/")









from .models import (
    tblIIIIbassets_authorization,
    tblIIIbprorations_schedule,
    tblCOMPANY,
    tblBRANCH,
    tblSTAFF,
    tblIIIbcoop,
    Userprofile,
    tblstandardsavingIIIB,
)

class SavePackTests(TestCase):
    def setUp(self):
        # Company and branch
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member")

        # Coop member
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, status=1, name="Coop Member")

        # Officer user profile
        self.userprofile = Userprofile.objects.create(
            email="testuser@example.com",
            status=1,
            thrift3b_officer=1,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )

        # Scheme standard
        self.scheme = "TestScheme"
        self.standard = tblstandardsavingIIIB.objects.create(
            branch=self.branch,
            description=self.scheme,
            to_month="December"
        )

        # Client with session
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKEPIN123")
    @patch("yourapp.views.savingscheme_email")
    def test_successful_save_pack(self, mock_email, mock_pin):
        url = reverse("save_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/mysavings_savings_schemee_success_o.html")

        # Authorization created
        auth = tblIIIIbassets_authorization.objects.get(
            branch=self.branch,
            staff=self.coop,
            description=self.scheme,
            status="Running",
            year="2026",
            month="January"
        )
        self.assertEqual(auth.asset_authorization_code, "FAKEPIN123")

        # Schedule created
        schedule = tblIIIbprorations_schedule.objects.filter(
            branch=self.branch,
            staff=self.coop,
            scheme=self.scheme,
            account_type="Assets",
            status="Awaiting Execution"
        )
        self.assertTrue(schedule.exists())
        self.assertEqual(schedule.first().authorization_code, "FAKEPIN123")

        # Email called
        mock_email.assert_called_once()

    def test_scheme_closed(self):
        url = reverse("save_pack")
        post_data = {
            "amount": "500",
            "scheme": self.scheme,
            "year": "2026",
            "month": "December",  # matches to_month
            "coop": self.coop.id,
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "This scheme is no longer open")

    def test_non_officer_redirects_to_404(self):
        # Create a non-officer user
        non_officer = Userprofile.objects.create(
            email="noofficer@example.com",
            status=1,
            thrift3b_officer=0,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_officer.email
        session.save()

        url = reverse("save_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()  # no session set
        url = reverse("save_pack")
        post_data = {
            "amount": "1000",
            "scheme": self.scheme,
            "year": "2026",
            "month": "January",
            "coop": self.coop.id,
        }
        response = client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/user/")






from .models import (
    tblCOMPANY,
    tblBRANCH,
    tblSTAFF,
    tblIIIbcoop,
    Userprofile,
    tblbusinessyear,
    tblmaxloanIIIB,
    tblstandardloanIIIB,
    tblIIIIbliabilities_authorization,
)

class ReqLoanTests(TestCase):
    def setUp(self):
        # Company and branch
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member", email="testuser@example.com", status=1)

        # Coop member
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)

        # Officer user profile
        self.userprofile = Userprofile.objects.create(
            email="testuser@example.com",
            status=1,
            thrift3b_officer=1,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )

        # Business year
        tblbusinessyear.objects.create(branch=self.branch, year="2026")

        # Max loan
        self.maxloan = tblmaxloanIIIB.objects.create(branch=self.branch, value=50)

        # Loan package
        self.loan_package = tblstandardloanIIIB.objects.create(branch=self.branch, description="Standard Loan", status=True)

        # Client with session
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKELOANPIN")
    @patch("yourapp.views.loanbook_email")
    @patch("yourapp.views.walletbalance", return_value=1000)
    def test_successful_reqloan_post(self, mock_balance, mock_email, mock_pin):
        url = reverse("reqloan")
        post_data = {
            "repayment": "1200",
            "principal": "1000",
            "package": "Standard Loan",
            "grace_period": "2",
            "interest": "200",
            "monthly_deduction": "100",
        }
        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/booking_officer_success.html")

        # Authorization created
        auth = tblIIIIbliabilities_authorization.objects.get(branch=self.branch, staff=self.coop)
        self.assertEqual(auth.application_code, "FAKELOANPIN")
        self.assertEqual(auth.status, "Awaiting Approval")

        # Email called
        mock_email.assert_called_once()

    @patch("yourapp.views.walletbalance", return_value=0)
    def test_empty_wallet(self, mock_balance):
        url = reverse("reqloan")
        response = self.client.get(url)
        self.assertContains(response, "Your wallet is empty.")
        self.assertTemplateUsed(response, "IIIb/myloans_apply_o1.html")

    @patch("yourapp.views.walletbalance", return_value=1000)
    def test_no_maxloan_set(self, mock_balance):
        # Delete max loan
        self.maxloan.delete()
        url = reverse("reqloan")
        response = self.client.get(url)
        self.assertContains(response, "maximum loan limit not set")
        self.assertTemplateUsed(response, "IIIb/myloans_apply_limit.html")

    def test_non_officer_redirects_to_404(self):
        non_officer = Userprofile.objects.create(
            email="noofficer@example.com",
            status=1,
            thrift3b_officer=0,
            thrift3b_admin=0,
            thrift3b_cashier=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_officer.email
        session.save()

        url = reverse("reqloan")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()  # no session set
        url = reverse("reqloan")
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/user/")





from .models import (
    tblCOMPANY,
    tblBRANCH,
    tblSTAFF,
    tblIIIbcoop,
    Userprofile,
    tblbusinessyear,
    tblIIIIbliabilities_authorization,
    tblIIIbapprovals,
    tblIIIbprorations,
    tblIIIbprorations_schedule,
    tblIIIbsavingsaccount,
    tblstandardsavingIIIB,
    tblIIIIbassets_authorization,
)

class LoanApprovalsTests(TestCase):
    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member", email="admin@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)

        # Admin user
        self.userprofile = Userprofile.objects.create(
            email="admin@example.com",
            status=1,
            thrift3b_admin=1,
            branch=self.branch,
            staffrec=self.staffrec
        )

        tblbusinessyear.objects.create(branch=self.branch, year="2026")

        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    def test_successful_loan_approval(self):
        # Create a pending liability
        tblIIIIbliabilities_authorization.objects.create(
            branch=self.branch,
            staff=self.coop,
            date=date(2026, 7, 1),
            status="Awaiting Approval",
            principal=1000
        )

        url = reverse("loan_approvals")
        post_data = {
            "year": "2026",
            "month_name": "July",
            "month_index": "7",
            "status": "Awaiting Approval"
        }
        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/approvalloan.html")

        # Approval created
        approval = tblIIIbapprovals.objects.get(branch=self.branch, month="July", year="2026")
        self.assertEqual(approval.status, "Approved")

    def test_already_approved(self):
        tblIIIbapprovals.objects.create(branch=self.branch, staff=self.coop, month="July", year="2026", status="Approved", amount=1000, transdate=date.today())
        url = reverse("loan_approvals")
        post_data = {
            "year": "2026",
            "month_name": "July",
            "month_index": "7",
            "status": "Awaiting Approval"
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "Approvals alreadydone for the July, 2026")
        self.assertTemplateUsed(response, "IIIb/approval_loan_error.html")

    def test_no_records_found(self):
        url = reverse("loan_approvals")
        post_data = {
            "year": "2026",
            "month_name": "August",
            "month_index": "8",
            "status": "Awaiting Approval"
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "No records found for August , 2026")
        self.assertTemplateUsed(response, "IIIb/approval_loan_error.html")

    def test_non_admin_redirects_to_404(self):
        non_admin = Userprofile.objects.create(
            email="user@example.com",
            status=1,
            thrift3b_admin=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_admin.email
        session.save()

        url = reverse("loan_approvals")
        response = client.get(url)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()
        url = reverse("loan_approvals")
        response = client.get(url)
        self.assertRedirects(response, "/login/user/")

class ProrationTests(TestCase):
    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member", email="admin@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)

        self.userprofile = Userprofile.objects.create(
            email="admin@example.com",
            status=1,
            thrift3b_admin=1,
            branch=self.branch,
            staffrec=self.staffrec
        )

        tblbusinessyear.objects.create(branch=self.branch, year="2026")
        tblstandardsavingIIIB.objects.create(branch=self.branch, description="SchemeA", to_month="December")

        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    def test_successful_proration(self):
        # Create awaiting schedule
        tblIIIbprorations_schedule.objects.create(
            branch=self.branch,
            staff=self.coop,
            month="July",
            year="2026",
            amount=500,
            transID="T123",
            authorization_code="AUTH123",
            scheme="SchemeA",
            account_type="Assets",
            status="Awaiting Execution"
        )

        url = reverse("proration")
        post_data = {
            "month_index": "7",
            "year": "2026"
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/proration_approv.html")

    def test_skip_month_fails(self):
        # Create awaiting schedule but simulate skip
        tblIIIbprorations.objects.create(branch=self.branch, staff=self.coop, month="June", year="2026", status="Executed", amount=100)
        tblIIIbprorations_schedule.objects.create(
            branch=self.branch,
            staff=self.coop,
            month="August",
            year="2026",
            amount=500,
            transID="T124",
            authorization_code="AUTH124",
            scheme="SchemeA",
            account_type="Assets",
            status="Awaiting Execution"
        )
        url = reverse("proration")
        post_data = {
            "month_index": "8",
            "year": "2026"
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "you cannot SKIP a Month")
        self.assertTemplateUsed(response, "IIIb/proration_fail.html")

    def test_already_prorated(self):
        tblIIIbprorations.objects.create(branch=self.branch, staff=self.coop, month="July", year="2026", status="Executed", amount=100)
        url = reverse("proration")
        post_data = {
            "month_index": "7",
            "year": "2026"
        }
        response = self.client.post(url, post_data)
        self.assertContains(response, "YOU ALREADY PRORATED FOR July, 2026")
        self.assertTemplateUsed(response, "IIIb/proration_fail.html")

    def test_non_admin_redirects_to_404(self):
        non_admin = Userprofile.objects.create(
            email="user@example.com",
            status=1,
            thrift3b_admin=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_admin.email
        session.save()

        url = reverse("proration")
        response = client.get(url)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()
        url = reverse("proration")
        response = client.get(url)
        self.assertRedirects(response, "/login/user/")






from .models import (
    tblCOMPANY,
    tblBRANCH,
    tblSTAFF,
    tblIIIbcoop,
    Userprofile,
    tblbusinessyear,
    tblIIIIbliabilities_authorization,
    tblIIIbsavingsaccount,
    tblIIIbprorations_schedule,
    tblIIIbdisbursals,
    tblstandardloanIIIB,
)

class LoanDisburseTests(TestCase):
    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Admin Staff", email="admin@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)

        # Admin user
        self.userprofile = Userprofile.objects.create(
            email="admin@example.com",
            status=1,
            thrift3b_admin=1,
            branch=self.branch,
            staffrec=self.staffrec
        )

        tblbusinessyear.objects.create(branch=self.branch, year="2026")

        # Loan package
        self.loan_package = tblstandardloanIIIB.objects.create(branch=self.branch, description="Loan Package", tenure=3)

        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKEPIN123")
    def test_successful_disburse(self, mock_pin):
        # Create liability awaiting approval
        liability = tblIIIIbliabilities_authorization.objects.create(
            branch=self.branch,
            staff=self.coop,
            date=date(2026, 7, 1),
            status="Awaiting Approval",
            principal=1000,
            thrift=100,
            grace_period=30,
            package=self.loan_package,
            application_code="APP123",
            description="Loan"
        )

        url = reverse("loan_disburse")
        post_data = {
            "year": "2026",
            "month_name": "July",
            "month_index": "7",
            "status": "Awaiting Approval"
        }
        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/payoutallaloan.html")

        # Liability status updated
        liability.refresh_from_db()
        self.assertEqual(liability.status, "Running")

        # Disbursal created
        disbursal = tblIIIbdisbursals.objects.get(branch=self.branch, month="July", year=2026)
        self.assertEqual(disbursal.status, "Disbursed")
        self.assertEqual(disbursal.amount, 1000)

    def test_no_liabilities_redirects_dashboard(self):
        url = reverse("loan_disburse")
        post_data = {
            "year": "2026",
            "month_name": "July",
            "month_index": "7",
            "status": "Awaiting Approval"
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, "/dashboard/")

    def test_non_admin_redirects_to_404(self):
        non_admin = Userprofile.objects.create(
            email="user@example.com",
            status=1,
            thrift3b_admin=0,
            branch=self.branch,
            staffrec=self.staffrec
        )
        client = Client()
        session = client.session
        session['userid'] = non_admin.email
        session.save()

        url = reverse("loan_disburse")
        response = client.get(url)
        self.assertTemplateUsed(response, "IIIb/404.html")

    def test_missing_session_redirects_to_login(self):
        client = Client()
        url = reverse("loan_disburse")
        response = client.get(url)
        self.assertRedirects(response, "/login/user/")

    def test_get_request_renders_payout_loan(self):
        url = reverse("loan_disburse")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/payout_loan.html")
