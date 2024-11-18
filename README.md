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

##### customersToday (after: 0, first: 0)
> return the list of customers registered today
>
##### idType (id)
> takes an id and returns the idType associated with the id
>
##### idTypes
> return the list of id types
>
##### simType (id)
> takes an id and returns the simType associated with the id
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
  > ![create_customer_mutation](https://github.com/user-attachments/assets/c1c282ab-a30b-4e33-ac4f-0a0c3d77c7bd)
  >
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

  
