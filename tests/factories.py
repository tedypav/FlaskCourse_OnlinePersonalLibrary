import random
import string
from random import randint

import factory

from db import db
from models import UserModel, ResourceModel, ResourceStatus, UserRole


class BaseFactory(factory.Factory):
    """
    A basic factory object that will be used for the other factories. It will be written in the database after creation.
    """
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class UserFactory(BaseFactory):
    """
    A factory to create valid users to be used in the tests.
    """

    class Meta:
        model = UserModel

    user_id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = "+359" + str(randint(100000000, 300000000))
    password = factory.Faker("password")
    company = "".join(random.choice(string.ascii_lowercase) for x in range(25))
    job_position = "".join(random.choice(string.ascii_lowercase) for x in range(25))
    user_role = UserRole.user


class ResourceFactory(BaseFactory):
    """
    A factory to create valid resources to be used in the tests.
    """

    class Meta:
        model = ResourceModel

    resource_id = factory.Sequence(lambda n: n)
    title = "".join(random.choice(string.ascii_lowercase) for i in range(120))
    author = "".join(random.choice(string.ascii_lowercase) for i in range(120))
    link = "".join(random.choice(string.ascii_lowercase) for i in range(120))
    notes = "".join(random.choice(string.ascii_lowercase) for i in range(120))
    rating = str(randint(1, 5))
    owner_id = factory.SubFactory(UserFactory)
    status = ResourceStatus.pending


class TagFactory(BaseFactory):
    """
    A factory to create valid tags to be used in the tests.
    """

    class Meta:
        model = ResourceModel

    tag_id = factory.Sequence(lambda n: n)
    tag = "".join(random.choice(string.ascii_lowercase) for i in range(50))
    owner_id = factory.SubFactory(UserFactory)
