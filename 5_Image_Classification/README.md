# Image Classification API

### Using: 
1. TensorFlow (for machine learning)
2. Keras (high level interface for tensorflow)
3. Keras InceptionsV3 
4. Pillow (to handle image data)

### API Chart Protocols
| Resource | Address   | Protocol | Parameters                    | Responses + status code                                                                                                    |
| -------- | --------- | -------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Register | /register | POST     | 1.username 2.password         | 200 OK 301 Invalid Username                                                                                                |
| Classify | /classify | POST     | 1.username 2.password 3.url   | 200 OK with predication +amount tokens left 301 Invalid Usernam 302 Invalid passowrd 303 Out of tokens 400 No URL provided |
| Refill   | /refill   | POST     | 1.username 2.adminPW 3.amount | 200 OK refilled 301 Invalid Username 304 Invalid admin passowrd                                                            |