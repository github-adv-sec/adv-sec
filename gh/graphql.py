get_ent_id = """
query enterprise ($slug: String!){ 
  enterprise (slug:$slug) {
    id
  }
}
"""

create_org = """
mutation createEnterpriseOrganization($adminLogins: [String!]!, $billingEmail: String!, $enterpriseId: ID!, $login: String!, $profileName: String!) {
  createEnterpriseOrganization(input: {enterpriseId: $enterpriseId, adminLogins: $adminLogins, billingEmail: $billingEmail, login: $login, profileName: $profileName}) {
    organization {
      id
      name
    }
  }
}
"""
