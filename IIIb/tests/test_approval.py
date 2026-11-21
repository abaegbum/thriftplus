from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import tblCOMPANY, tblBRANCH, tblSTAFF, tblIIIbcoop, Userprofile, tblbusinessyear, tblIIIIbliabilities_authorization, tblIIIbapprovals

class LoanApprovalsTests(TestCase):
    """Tests for the loan_approvals view"""

    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Admin Staff", email="admin@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)
        self.userprofile = Userprofile.objects.create(email="admin@example.com", status=1, thrift3b_admin=1, branch=self.branch, staffrec=self.staffrec)
        tblbusinessyear.objects.create(branch=self.branch, year="2026")
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    def test_successful_loan_approval(self):
        """Admin can approve loans successfully"""
        tblIIIIbliabilities_authorization.objects.create(branch=self.branch, staff=self.coop, date=date(2026, 7, 1), status="Awaiting Approval", principal=1000)
        url = reverse("loan_approvals")
        post_data = {"year": "2026", "month_name": "July", "month_index": "7", "status": "Awaiting Approval"}
        response = self.client.post(url, post_data)
        self.assertTemplateUsed(response, "IIIb/approvalloan.html")
        self.assertTrue(tblIIIbapprovals.objects.filter(branch=self.branch, month="July", year="2026").exists())
