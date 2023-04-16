from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
from service.models import ServiceRequest, RepairService


class TestCreateServiceView(TestCase):
    def setUp(self):
        self.client = Client()

        # create sample user
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="testpass"
        )

        # create repair service
        self.repair_service = RepairService.objects.create(
            service_type="Mobile", device_type="samsung", base_cost=1000
        )

        self.client.login(email="testuser@gmail.com", password="testpass")
        self.url = reverse("service_request_create")

    def test_create_service_request(self):
        data = {
            "title": "Test Service Request",
            "description": "This is a test service request",
            "repair_service": self.repair_service.pk,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServiceRequest.objects.count(), 1)
        service_request = ServiceRequest.objects.first()
        self.assertEqual(service_request.title, "Test Service Request")
        self.assertEqual(
            service_request.description,
            "This is a test service request",
        )
        self.assertEqual(service_request.repair_service, self.repair_service)
        self.assertEqual(service_request.User, self.user)

    def test_create_service_with_missing_title(self):
        # Test missing title field
        data = {
            "description": "This is a test service request",
            "repair_service": self.repair_service.pk,
        }
        response = self.client.post(self.url, data)
        self.assertContains(response, "This field is required.")

    def test_create_service_with_missing_repair_service(self):
        # Test missing repair_service field
        data = {
            "title": "Test Service Request",
            "description": "This is a test service request",
        }
        response = self.client.post(self.url, data)
        self.assertContains(response, "This field is required.")


class TestHomePageView(TestCase):
    """
    Test class for the home page view.

    Tests whether authenticated staff and superusers can access the home page, while non-staff and unauthenticated
    users are redirected to the service request list page.
    """

    def setUp(self):
        """
        Setup method that initializes a client, url, and creates a staff user for testing.
        """
        self.client = Client()
        self.url = reverse("home")
        self.user = User.objects.create_staff(
            email="testuser@gmail.com", password="testpass"
        )

    def test_authenticated_staff_user_can_access_home_page(self):
        """
        Test that an authenticated staff user can access the home page and the correct template is rendered.
        """
        self.client.login(email="testuser@gmail.com", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_authenticated_non_staff_user_cannot_access_home_page(self):
        """
        Test that an authenticated non-staff user is redirected to the service request list page when trying to
        access the home page.
        """
        User.objects.create_user(email="nonstaffuser@gmail.com", password="testpass")
        self.client.login(email="nonstaffuser@gmail.com", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("service_request_list"))

    def test_unauthenticated_user_cannot_access_home_page(self):
        """
        Test that an unauthenticated user is redirected to the login page with the next parameter set to the home
        page when trying to access the home page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")

    def test_admin_can_access_home_page(self):
        """
        Test that a superuser can access the home page and the correct template is rendered.
        """
        User.objects.create_superuser(email="admin@gmail.com", password="testpass")
        self.client.login(email="admin@gmail.com", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class TestLandingPageView(TestCase):

    """
    Test class for the landing page view.

    Tests whether the landing page is rendered successfully.
    """

    def setUp(self):
        """
        Setup method that initializes a client and url for testing.
        """
        self.client = Client()
        self.url = reverse("landing")

    def test_landing_page_renders_successfully(self):
        """
        Test that the landing page is rendered successfully and the correct template is used.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")
