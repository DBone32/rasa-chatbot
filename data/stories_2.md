## normal story
* greet
  - utter_greet
* ask_cost
  - get_cost_form
* thank
  - utter_thank
* goodbye
  - utter_goodbye

## ask cost 1
* ask_cost
  - get_cost_form
* thank
  - utter_thank

## ask cost 2
* ask_cost
  - get_cost_form
* ask_cost
  - get_cost_form
* thank
  - utter_thank

## ren_house
* ren_house
  - ren_house_form
* ren_house
  - ren_house_form
* thank
  - utter_thank

## ren_house 2
* ren_house
  - buy_house_form
* ren_house
  - buy_house_form
* thank
  - utter_thank

## buy_house
* buy_house
  - buy_house_form
* buy_house
  - buy_house_form
* thank
  - utter_thank

## buy_house
* greet
  - utter_greet
* buy_house
  - buy_house_form
* thank
  - utter_thank

## thank
* thank
  - utter_thank

## say goodbye
* goodbye
  - utter_goodbye

## New Story

* greet
    - utter_greet
* buy_house{"estate_type":"chung cư"}
    - slot{"estate_type":"chung cư"}
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"chung cư"}
    - slot{"estate_type":"chung cư"}
    - slot{"requested_slot":"address"}
* buy_house{"address":"cầu giấy"}
    - slot{"address":"cầu giấy"}
    - buy_house_form
    - slot{"address":"cầu giấy"}
    - slot{"requested_slot":"cost"}
* info_price{"cost":"2-3 tỷ"}
    - slot{"cost":"2-3 tỷ"}
    - buy_house_form
    - slot{"cost":"2-3 tỷ"}
    - form{"name":null}
    - slot{"requested_slot":null}
* thank
    - utter_thank

## New Story

* greet
    - utter_greet
* buy_house{"estate_type":"chung cư","address":"ngã tư sở"}
    - slot{"address":"ngã tư sở"}
    - slot{"estate_type":"chung cư"}
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"chung cư"}
    - slot{"address":"ngã tư sở"}
    - slot{"estate_type":"chung cư"}
    - slot{"address":"ngã tư sở"}
    - slot{"requested_slot":"cost"}
* info_price{"cost":"9 tỷ"}
    - slot{"cost":"9 tỷ"}
    - buy_house_form
    - slot{"cost":"9 tỷ"}
    - form{"name":null}
    - slot{"requested_slot":null}
* thank
    - utter_thank

## New Story

* greet
    - utter_greet
* ren_house{"estate_type":"chung cư","cost":"8tr"}
    - slot{"cost":"8tr"}
    - slot{"estate_type":"chung cư"}
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"chung cư"}
    - slot{"cost":"8tr"}
    - slot{"estate_type":"chung cư"}
    - slot{"cost":"8tr"}
    - slot{"requested_slot":"address"}
* info_location{"address":"Đống Đa"}
    - slot{"address":"Đống Đa"}
    - buy_house_form
    - slot{"address":"Đống Đa"}
    - form{"name":null}
    - slot{"requested_slot":null}
* thank
    - utter_thank

## New Story

* ask_cost{"estate_type":"chung cư","address":"Hà Đông","cost":"4-5 tỷ"}
    - slot{"address":"Hà Đông"}
    - slot{"cost":"4-5 tỷ"}
    - slot{"estate_type":"chung cư"}
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"chung cư"}
    - slot{"address":"Hà Đông"}
    - slot{"cost":"4-5 tỷ"}
    - slot{"estate_type":"chung cư"}
    - slot{"address":"Hà Đông"}
    - slot{"cost":"4-5 tỷ"}
    - form{"name":null}
    - slot{"requested_slot":null}
* thank
    - utter_thank

## New Story

* ren_house{"estate_type":"phòng trọ","address":"trần duy hưng"}
    - slot{"address":"trần duy hưng"}
    - slot{"estate_type":"phòng trọ"}
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"phòng trọ"}
    - slot{"address":"trần duy hưng"}
    - slot{"estate_type":"phòng trọ"}
    - slot{"address":"trần duy hưng"}
    - slot{"requested_slot":"cost"}
* info_price{"cost":"3tr"}
    - slot{"cost":"3tr"}
    - buy_house_form
    - slot{"cost":"3tr"}
    - form{"name":null}
    - slot{"requested_slot":null}
* info_price
    - buy_house_form
    - form{"name":"buy_house_form"}
    - slot{"estate_type":"phòng trọ"}
    - slot{"address":"trần duy hưng"}
    - slot{"cost":"3tr"}
    - form{"name":null}
    - slot{"requested_slot":null}
