from django.test import TestCase, Client
from django.urls import reverse
from .models import tblCOMPANY, tblBRANCH, tblSTAFF, tblIIIbcoop, Userprofile, tblbusinessyear, tblstandardsavingIIIB, tblIIIbprorations_schedule

class ProrationTests(TestCase):
    """Tests for the proration view"""

    def setUp(self):
        self.company = tblCOMPANY.objects.create(name="TestCo")
        self.branch = tblBRANCH.objects.create(company=self.company, name="Main Branch")
        self.staffrec = tblSTAFF.objects.create(branch=self.branch, name="Admin Staff", email="admin@example.com", status=1)
        self.coop = tblIIIbcoop.objects.create(branch=self.branch, staff=self.staffrec, status=1)
        self.userprofile = Userprofile.objects.create(email="admin@example.com", status=1, thrift3b_admin=1, branch=self.branch, staffrec=self.staffrec)
        tblbusinessyear.objects.create(branch=self.branch, year="2026")
        tblstandardsavingIIIB.objects.create(branch=self.branch, description="SchemeA", to_month="December")
        self.client = Client()
        session = self.client.session
        session['userid'] = self.userprofile.email
        session.save()

    def test_successful_proration(self):
        """Admin can execute proration successfully"""
        tblIIIbprorations_schedule.objects.create(branch=self.branch, staff=self.coop, month="July", year="2026", amount=500, transID="T123", authorization_code="AUTH123", scheme="SchemeA", account_type="Assets", status="Awaiting Execution")
        url = reverse("proration")
        post_data = {"month_index": "7", "year": "2026"}
        response = self.client.post(url, post_data)
        self.assertTemplateUsed(response, "IIIb/proration_approv.html")
