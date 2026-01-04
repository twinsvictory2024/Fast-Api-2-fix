import requests


# responce = requests.post('http://localhost:8000/user/', 
#                          json={"name": "admin",
#                                "password": "1234"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.post('http://localhost:8000/user/', 
#                          json={"name": "first_user",
#                                "password": "5678"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.post('http://localhost:8000/user/', 
#                          json={"name": "second_user",
#                                "password": "9876"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/user/', 
#                          json={"name": "third_user",
#                                "password": "7777"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")



# responce = requests.post('http://localhost:8000/login/', 
#                          json={"name": "admin",
#                                "password": "1234"
#                                })
# token1 = responce.json()["token"]
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.post('http://localhost:8000/login/', 
#                          json={"name": "second_user",
#                                "password": "9876"
#                                })
# token2 = responce.json()["token"]
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.post('http://localhost:8000/login/', 
#                          json={"name": "third_user",
#                                "password": "7777"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")
# token3 = responce.json()["token"]



# responce = requests.patch('http://localhost:8000/user/4/', 
#                          json={"name": "third_user_fix",
#                                "password": "8888"
#                                })
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.patch('http://localhost:8000/user/4/', 
#                          json={"name": "third_user_fix",
#                                "password": "8888"
#                                },
#                         headers={"x-token": token1})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.delete('http://localhost:8000/user/6/',
#                         headers={"x-token": token3})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.post('http://localhost:8000/advertisement', 
#                         json={"title": "ad_1",
#                                "description": "Ad descr 1",
#                                "price": 1337
#                                },
#                         headers={"x-token": token1})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/advertisement', 
#                          json={"title": "ad_2",
#                                "description": "Ad descr 2",
#                                "price": 7331
#                                },
#                         headers={"x-token": token2})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/advertisement', 
#                          json={"title": "3rd AD",
#                                "description": "Ad descr 3",
#                                "price": 12345
#                                },
#                         headers={"x-token": token1})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/advertisement', 
#                          json={"title": "4rt AD",
#                                "description": "Ad descr four",
#                                "price": 78423
#                                },
#                         headers={"x-token": token2})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/advertisement', 
#                          json={"title": "5th AD",
#                                "description": "Ad descr 5",
#                                "price": 23456
#                                },
#                         headers={"x-token": token1})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.post('http://localhost:8000/advertisement', 
#                          json={"title": "6th AD",
#                                "description": "Ad descr 6",
#                                "price": -23456
#                                },
#                         headers={"x-token": token2})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")


# responce = requests.patch('http://localhost:8000/advertisement/2', 
#                          json={"title": "FIXED ADVERTISEMENT",
#                                "description": "Ad descr FIXED",
#                                "price": 98765
#                                },
#                         headers={"x-token": token2})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# # responce = requests.get('http://localhost:8000/advertisement/?description=four&limit=2')
# # print(f"Responce: {responce.text}")
# # print(f"HTTP code: {responce.status_code}")

# responce = requests.get('http://localhost:8000/advertisement/5/')
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")

# responce = requests.delete('http://localhost:8000/advertisement/5/', headers={"x-token": token1})
# print(f"Responce: {responce.text}")
# print(f"HTTP code: {responce.status_code}")