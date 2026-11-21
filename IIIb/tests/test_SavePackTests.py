from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import tblCOMPANY, tblBRANCH, tblSTAFF, tblIIIbcoop, Userprofile, tblstandardsavingIIIB, tblIIIIbassets_authorization, tblIIIbprorations_schedule

class SavePackTests(TestCase):
    """Tests for the save_pack view"""

    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Staff Member", email="testuser@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, status=1, staff=self.staffrec)
        self.userprofile = Userprofile.objects.create(email="testuser@example.com", status=1, thrift3b_officer=1, branch=self.branch, staffrec=self.staffrec)
        self.scheme = "TestScheme"
        tblstandardsavingIIIB.objects.create(branch=self.branch, description=self.scheme, to_month="December")
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    @patch("yourapp.views.generate_trans_pin", return_value="FAKEPIN123")
    @patch("yourapp.views.savingscheme_email")
    def test_successful_save_pack(self, mock_email, mock_pin):
        """Officer can create authorization and schedule successfully"""
        url = reverse("save_pack")
        post_data = {"amount": "1000", "scheme": self.scheme, "year": "2026", "month": "January", "coop": self.coop.id}
        response = self.client.post(url, post_data)
        self.assertTemplateUsed(response, "IIIb/mysavings_savings_schemee_success_o.html")
        self.assertTrue(tblIIIIbassets_authorization.objects.filter(branch=self.branch, staff=self.coop).exists())
        mock_email.assert_called_once()
