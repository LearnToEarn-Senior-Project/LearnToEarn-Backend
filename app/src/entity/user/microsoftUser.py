import msal


class MicrosoftUser(object):
    clientId = "d12aa2d5-52fe-4678-9a4a-c5211dee54c7"
    clientSecret = "b11b4201-09b2-45ad-959a-cfa355a4cf23"
    redirectUri = "http://localhost:3000/auth"
    SCOPE = [
        "User.Read",
        "Team.ReadBasic.All",
        "TeamSettings.Read.All",
        "TeamSettings.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All", ]

    @staticmethod
    def getUserToken(authority=None):
        cache = msal.SerializableTokenCache()
        cca = msal.ConfidentialClientApplication(
            MicrosoftUser.clientId, authority=authority,
            client_credential=MicrosoftUser.clientSecret, token_cache=cache)
        accounts = cca.get_accounts()
        if accounts:
            result = cca.acquire_token_silent(MicrosoftUser.SCOPE, account=accounts[0])
            print(result)
            return result
