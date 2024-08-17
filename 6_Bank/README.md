# Bank API

### Using: 
1. 
2. 

### API Chart Protocols
| Resource      | Address   | Protocol | Parameters                                   | Responses + status code                          |
| ------------- | --------- | -------- | -------------------------------------------- | ------------------------------------------------ |
| Register      | /register | POST     | 1.username 2.password                        | 200-OK 301-Invalid Username 302-Invalid password |
| Add           | /add      | POST     | 1.username 2.password 3.amount               | 200 301 302 304-Negative money amount            |
| Transfer      | /transfer | POST     | 1.username 2.password 3.to {acount} 4.amount | 200 301 302 303-not enough money 304             |
| Check Balance | /balance  | POST     | 1.username 2.password                        | 200 301 302                                      |
| Take Loan     | /takeloan | POST     | 1.username 2.password 3.amount               | 200 301 302 304                                  |
| Pay Loan      | /payloan  | POST     | 1.username 2.password 3.amount               | 200 301 302 303 304                              |