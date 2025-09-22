# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from django.urls import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
# from .models import Agent, Type, Property, PropertyAlbum


# class RealEstateTests(TestCase):
#     def setUp(self):
#         """Setup test data for all tests"""
#         # Create a user for agent
#         self.user = User.objects.create_user(username="agent1", password="test123")

#         # Create Agent
#         self.agent = Agent.objects.create(
#             user=self.user,
#             name="John Agent",
#             email="john@example.com",
#             contacts="0700000000",
#             description="A very good agent in Kampala"
#         )

#         # Create Property Type
#         self.type = Type.objects.create(name="House")

#         # Create a dummy image for Property
#         self.property_image = SimpleUploadedFile(
#             name="property.jpg",
#             content=b"file_content",
#             content_type="image/jpeg"
#         )

#         # Create Property
#         self.property = Property.objects.create(
#             name="Dream House",
#             agent=self.agent,
#             price=120000.0,
#             type=self.type,
#             description="A nice 3-bedroom house",
#             size=200.5,
#             bedrooms=3,
#             bathrooms=2,
#             location="Kampala",
#             selrent="sell",
#             picture=self.property_image
#         )

#         # Create a dummy image for PropertyAlbum
#         self.album_image_file = SimpleUploadedFile(
#             name="album1.jpg",
#             content=b"album_file_content",
#             content_type="image/jpeg"
#         )

#         # Create Property Album Image
#         self.album_image = PropertyAlbum.objects.create(
#             property=self.property,
#             image=self.album_image_file
#         )

#         # Client for views
#         self.client = Client()

#     # -----------------------------
#     # Model Tests
#     # -----------------------------
#     def test_agent_creation(self):
#         self.assertEqual(self.agent.name, "John Agent")
#         self.assertEqual(self.agent.user.username, "agent1")
#         self.assertIn("john@", self.agent.email)

#     def test_type_creation(self):
#         self.assertEqual(self.type.name, "House")

#     def test_property_creation(self):
#         self.assertEqual(self.property.name, "Dream House")
#         self.assertEqual(self.property.agent, self.agent)
#         self.assertEqual(self.property.type, self.type)
#         self.assertGreater(self.property.price, 0)
#         self.assertEqual(self.property.bedrooms, 3)
#         self.assertEqual(self.property.bathrooms, 2)

#     def test_property_str(self):
#         self.assertEqual(str(self.property), "Dream House-- Kampala")

#     def test_property_album_creation(self):
#         self.assertEqual(self.album_image.property, self.property)
#         self.assertIn("Album Image", str(self.album_image))

#     def test_property_negative_price(self):
#         """Ensure negative price is stored (no validator applied yet)"""
#         bad_property_image = SimpleUploadedFile(
#             name="bad_property.jpg",
#             content=b"file_content",
#             content_type="image/jpeg"
#         )
#         bad_property = Property.objects.create(
#             name="Invalid House",
#             agent=self.agent,
#             price=-500,
#             type=self.type,
#             description="Invalid property",
#             size=50,
#             bedrooms=1,
#             bathrooms=1,
#             location="Entebbe",
#             selrent="rent",
#             picture=bad_property_image
#         )
#         self.assertTrue(bad_property.price < 0)

#     # -----------------------------
#     # View Tests
#     # -----------------------------
#     def test_property_list_view(self):
#         """Check if property list page works"""
#         try:
#             response = self.client.get(reverse("listings"))
#             self.assertEqual(response.status_code, 200)
#             self.assertContains(response, "Dream House")
#         except Exception:
#             self.skipTest("Listings view not defined in urls.py")

#     def test_property_registration_requires_login(self):
#         """Check if property registration page requires login"""
#         try:
#             response = self.client.get(reverse("propertyregistration"))
#             # Should redirect to login if not authenticated
#             self.assertNotEqual(response.status_code, 200)
#         except Exception:
#             self.skipTest("Property registration view not defined in urls.py")


from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Agent, Type, Property, PropertyAlbum
from .forms import AgentForm, PropertyForm


class RegressionTests(TestCase):
    def setUp(self):
        """Setup test data for regression tests"""

        # Create Groups
        self.agent_group, _ = Group.objects.get_or_create(name="Agents")

        # Create user and assign to Agent group
        self.user = User.objects.create_user(username="agent1", password="test123")
        self.user.groups.add(self.agent_group)

        # Create Agent linked to user
        self.agent = Agent.objects.create(
            user=self.user,
            name="John Agent",
            email="john@example.com",
            contacts="0700000000",
            description="A top agent in Kampala"
        )

        # Create Property Type
        self.type = Type.objects.create(name="House")

        # Dummy image for Property
        self.property_image = SimpleUploadedFile(
            name="property.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )

        # Create Property
        self.property = Property.objects.create(
            name="Dream House",
            agent=self.agent,
            price=120000.0,
            type=self.type,
            description="A nice 3-bedroom house",
            size=200.5,
            bedrooms=3,
            bathrooms=2,
            location="Kampala",
            selrent="sell",
            picture=self.property_image
        )

        # Dummy image for PropertyAlbum
        self.album_image_file = SimpleUploadedFile(
            name="album1.jpg",
            content=b"album_file_content",
            content_type="image/jpeg"
        )

        # Create Property Album Image
        self.album_image = PropertyAlbum.objects.create(
            property=self.property,
            image=self.album_image_file
        )

        # Client for views
        self.client = Client()

    # -----------------------------
    # Model Regression Tests
    # -----------------------------
    def test_agent_model(self):
        """Agent model regression test"""
        self.assertEqual(self.agent.name, "John Agent")
        self.assertEqual(self.agent.user.username, "agent1")
        self.assertIn("john@", self.agent.email)

    def test_property_type_model(self):
        """Property Type regression test"""
        self.assertEqual(self.type.name, "House")

    def test_property_model(self):
        """Property model regression test"""
        self.assertEqual(self.property.name, "Dream House")
        self.assertEqual(self.property.agent, self.agent)
        self.assertEqual(self.property.type, self.type)
        self.assertGreater(self.property.price, 0)
        self.assertEqual(self.property.bedrooms, 3)
        self.assertEqual(self.property.bathrooms, 2)

    def test_property_str_method(self):
        """Check Property __str__ output"""
        self.assertEqual(str(self.property), "Dream House-- Kampala")

    def test_property_album_model(self):
        """PropertyAlbum regression test"""
        self.assertEqual(self.album_image.property, self.property)
        self.assertIn("Album Image", str(self.album_image))

    def test_negative_price_property(self):
        """Ensure negative price is stored (no validator applied yet)"""
        bad_property_image = SimpleUploadedFile(
            name="bad_property.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        bad_property = Property.objects.create(
            name="Invalid House",
            agent=self.agent,
            price=-500,
            type=self.type,
            description="Invalid property",
            size=50,
            bedrooms=1,
            bathrooms=1,
            location="Entebbe",
            selrent="rent",
            picture=bad_property_image
        )
        self.assertTrue(bad_property.price < 0)

    # -----------------------------
    # View Regression Tests
    # -----------------------------
    def test_property_list_view(self):
        """Property list page should render and include property name"""
        response = self.client.get(reverse("listings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dream House")

    def test_property_registration_requires_login(self):
        """Property registration page requires login"""
        response = self.client.get(reverse("propertyregistration"))
        self.assertNotEqual(response.status_code, 200)  # Should redirect

    def test_agent_dashboard_requires_login(self):
        """Agent dashboard requires login"""
        response = self.client.get(reverse("agentdb"))
        self.assertNotEqual(response.status_code, 200)

    # -----------------------------
    # Form Regression Tests
    # -----------------------------
    def test_agent_registration_form_valid(self):
        """AgentRegistrationForm should validate correctly"""
        form_data = {
            "name": "New Agent",
            "email": "new@example.com",
            "contacts": "0711111111",
            "description": "New agent description"
        }
        form = AgentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_property_form_valid(self):
        """PropertyForm should validate and save correctly"""
        form_data = {
            "name": "Luxury House",
            "agent": self.agent.id,
            "type": self.type.id,
            "price": 500000,
            "selrent": "sell",
            "location": "Kampala",
            "size": 250,
            "bedrooms": 4,
            "bathrooms": 3
        }
        form_files = {"picture": self.property_image}
        form = PropertyForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_property_form_invalid_negative_price(self):
        """PropertyForm should fail on negative price"""
        form_data = {
            "name": "Bad House",
            "agent": self.agent.id,
            "type": self.type.id,
            "price": -1000,
            "selrent": "sell",
            "location": "Kampala",
            "size": 100,
            "bedrooms": 2,
            "bathrooms": 1
        }
        form_files = {"picture": self.property_image}
        form = PropertyForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
