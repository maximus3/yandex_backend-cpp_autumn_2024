import random

from fake import provider

from enterprise.models import User, Job, Company


if __name__ == "__main__":
    for locale in provider.LOCALES:
        try:
            fake = provider.fake(locale)

            companies = Company.bulk_create(
                Company(title=fake.company(), address=fake.address())
                for _ in range(200)
            )
            jobs = Job.bulk_create(
                Job(title=fake.job()) for _ in range(100)
            )

            if hasattr(fake, "middle_name"):
                middle_name = fake.middle_name()
            else:
                middle_name = ""

            User.bulk_create(
                [
                    User(
                        first_name=fake.first_name(),
                        second_name=middle_name,
                        last_name=fake.last_name(),
                        email=fake.email(),
                        address=fake.address(),
                        phone_number=fake.phone_number(),
                        company=random.choice(companies),
                        job=random.choice(jobs),
                    )
                    for _ in range(30000)
                ],
            )
            print(locale)
        except Exception as err:
            print(locale)
            print(str(err))

    print("Successfully")
