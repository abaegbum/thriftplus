from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from datetime import date
from .models import tblCOMPANY, tblBRANCH, tblSTAFF, tblIIIbcoop, Userprofile, tblbusinessyear, tblmaxloanIIIB, tblstandardloanIIIB, tblIIIIbliabilities_authorization

class ReqLoanTests(TestCase):
    """Tests for the reqloan view"""

    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member", email="testuser@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)
        self.userprofile = Userprofile.objects.create(email="testuser@example.com", status=1, thrift3b_officer=1, branch=self.branch, staffrec=self.staffrec)
        tblbusinessyear.objects.create(branch=self.branch, year="2026")
        tblmaxloanIIIB.objects.create(branch=self.branch, value=50)
        tblstandardloanIIIB.objects.create(branch=self.branch, description="Standard Loan", status=True)
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKELOANPIN")
    @patch("yourapp.views.loanbook_email")
    @patch("yourapp.views.walletbalance", return_value=1000)
    def test_successful_reqloan_post(self, mock_balance, mock_email, mock_pin):
        """Officer can apply for a loan successfully"""
        url = reverse("reqloan")
        post_data = {"repayment": "1200", "principal": "1000", "package": "Standard Loan", "grace_period": "2", "interest": "200", "monthly_deduction": "100"}
        response = self.client.post(url, post_data)
        self.assertTemplateUsed(response, "IIIb/booking_officer_success.html")
        self.assertTrue(tblIIIIbliabilities_authorization.objects.filter(branch=self.branch, staff=self.coop).exists())
        mock_email.assert_called_once()
