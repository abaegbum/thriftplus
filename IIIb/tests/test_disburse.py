from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from datetime import date
from yourapp.models import (
    tblCOMPANY, tblBRANCH, tblSTAFF, tblIIIbcoop, Userprofile,
    tblbusinessyear, tblIIIIbliabilities_authorization,
    tblIIIbsavingsaccount, tblIIIbprorations_schedule,
    tblIIIbdisbursals, tblstandardloanIIIB
)

class LoanDisburseTests(TestCase):
    """Tests for the loan_disburse view"""

    def setUp(self):
        # Company, branch, staff
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

        # Business year and loan package
        tblbusinessyear.objects.create(branch=self.branch, year="2026")
        self.loan_package = tblstandardloanIIIB.objects.create(branch=self.branch, description="Loan Package", tenure=3)

        # Client with session
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKEPIN123")
    def test_successful_disburse(self, mock_pin):
        """Admin can disburse loans successfully"""
        # Liability awaiting approval
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

        # Correct template rendered
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "IIIb/payoutallaloan.html")

        # Liability updated
        liability.refresh_from_db()
        self.assertEqual(liability.status, "Running")

        # Savings account debit created
        self.assertTrue(tblIIIbsavingsaccount.objects.filter(branch=self.branch, staff=self.coop, status="DR").exists())

        # Repayment schedule created
        self.assertTrue(tblIIIbprorations_schedule.objects.filter(branch=self.branch, staff=self.coop, account_type="Liabilities").exists())

        # Disbursal record created
        self.assertTrue(tblIIIbdisbursals.objects.filter(branch=self.branch, month="July", year=2026, status="Disbursed").exists())
