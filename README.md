# qcell-sim-registration
Register your qcell sim.

## API
We are using the graphql api which nicely blends with django.

### Endpoints
  - /graphql

    First send a request to the login mutation with a valid username and password and
    get a jwt_token in return.
    Use the token for every subsequent request.

#### Query
  - customer
  - customers
  - customersToday
  - idType
  - idTypes
  - simType
  - simTypes
  - totalSims
  - totalStandardSims

  ##### customer (id)
  > takes an id and returns the customer associated with id
> 
  ##### customers (after:0, first:0, when:"")
  > return a list of customers
  >
  > `after` and `first` are for pagination
  >
  > after: 2 - means retrive all customers after the first two
  >
  > first: 2 - means retrive the first two customers
  >
  > after: 4, first: 4 - means retrive 4 customers after the first 4 / starting after the first 4
  >
  > when: example 1. when: 'yesterday' 2. when: '2daysago'

##### customersToday (after: 0, first: 0)
> return the list of customers registered today
>
##### idTypes
> return the list of id types
>
##### simTypes
> return the list of sim types
>
##### totalEsims
> return the total esims registered
>
##### totalStandardSims
> return the total standard sims registered
> 
##### totalSims
> return the total sims registered (eSim + standard sim)
>

#### Mutations
  - createCustomer
  - deleteCustomer
  - file
  - login
  - refreshToken
  - searchNumber
  - tokenAuth
  - verifyToken

  ##### createCustomer
  > creates a customer
  >
  > required field
  > 
  > ![create-customer-mutation](https://github.com/user-attachments/assets/ee0dae43-0667-4d88-a79c-158cc6fc6a14)

  ###### Note on Gender field:
  >
  > currently it takes `male` and `female` in the following shape:
  >
    Male:
      male
      Male
      MALE
      m
      M

    Female:
      female
      Female
      FEMALE
      F
      f

  ###### Note on IdType field:
  >
  > currently it takes `license`, `national id`, `voters id` and `passport` in the following shape:
  > 
  -  License
  > `License` `license` `LICENSE` `lic` `LIC`
  >
  - Passport
  > `Passport` `passport` `PASSPORT` `PP` `PP`
  >
  - National Id
  > `NIN`, `nin`, `national_id`,
    `Voters_id`, `National_ID`,
    `national ID`, `National ID`,
    `national id`, `NATIONAL ID`
    `nationalid`, `NATIONALID`
  >
  - Voters Id
  > `VI`, `vi`, `voters_id`,
    `Voters_id`, `Voters_ID`,
    `voters ID`, `Voters ID`,
    `voters id`, `VOTERS ID`
    `votersid`, `VOTERSID`

  ###### Note on SimType field:
  >
  > currently it takes `Standard sim` and `Embedded sim` in the following shape:
  > 
  - Embedded Sim
  > `esim`,
    `Esim`,
    `ESIM`,
  - Standard Sim
  > `standard_sim`, `standard sim`,
    `Standard Sim`, `STANDARDSIM`,
    `standardsim`, `standard_sim`,
    `standard`, `Standard`, `STANDARD`

  ##### deleteCustomer
  > takes an id and deletes a customer
  >
  ##### file
  > upload a file (this will be used for the national id image)
  >
  > `note` that the endpoint is /graphql/file_upload
  >
  ##### searchNumber
  > takes a required field
  >
  > - number
  > - simTypeId

  
