from rest_framework.throttling import UserRateThrottle


# this is throttling for api , not global
class ProductListThrottle(UserRateThrottle):
    rate = "10/min"


class ProductCreateThrottle(UserRateThrottle):
    rate = "5/min"
