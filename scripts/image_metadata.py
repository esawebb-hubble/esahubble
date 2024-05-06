from djangoplicity.media.models import Image


def replace_creator_metadata(queryset):
    if queryset.count() > 0:
        try:
            queryset.update(
                creator='ESA/Hubble',
                creator_url='https://esahubble.org',
                contact_address='ESA Office, Space Telescope Science Institute, 3700 San Martin Dr',
                contact_city='Baltimore',
                contact_state_province='MD',
                contact_postal_code='21218',
                contact_country='United States',
                rights='Creative Commons Attribution 4.0 International License',
            )
            print('Successfully replace {} creator metadata'.format(queryset.count()))
        except Exception:
            print('Error replacing creator metadata')

print("Replacing images creator metadata information")
queryset = Image.objects.all()
replace_creator_metadata(queryset)
