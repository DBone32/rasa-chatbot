## Tài khoản 8
* login_failed
    - utter_login_failed
* login_failed
    - utter_login_failed
    - utter_how_contact_customer_service

## Tài khoản 9
* login_failed
    - utter_login_failed
* deny
    - utter_how_contact_customer_service

## Tài khoản 10
* lost_otp
    - utter_lost_otp
* deny
    - utter_how_contact_customer_service

## Tài khoản 12
* lost_otp
    - utter_lost_otp
* lost_otp
    - utter_lost_otp
    - utter_how_contact_customer_service

## Tài khoản 14
* channel_app
    - utter_channel_app
* how_download_or_view_st
    - utter_how_download_app

## Hạ tin-Hoàn tiền 2
* request_down_post
    - utter_bot_need_info_for_refund
    - calculate_down_post_form
    - form{"name": "calculate_down_post_form"}
    - form{"name": null}

## Hạ tin-Hoàn tiền 3
* request_down_post
    - utter_bot_need_info_for_refund
    - calculate_down_post_form
    - form{"name":"calculate_down_post_form"}
    - slot{"requested_slot":"source_post_package"}
* canthelp OR deny
    - action_deactivate_form
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirm
    - utter_anything_else

## Hạ tin-Hoàn tiền 4
* request_change_post_package
    - utter_bot_need_info_for_change_source_package
    - calculate_change_post_form
    - form{"name": "calculate_change_post_form"}
    - form{"name": null}

## Hạ tin-Hoàn tiền 5
* request_change_post_package
    - utter_bot_need_info_for_change_source_package
    - calculate_change_post_form
    - form{"name":"calculate_change_post_form"}
    - slot{"requested_slot":"source_post_package"}
* canthelp OR deny
    - action_deactivate_form
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_confirm
    - utter_anything_else

## Meey Invest 1
* how_invest_to_meeyland
    - utter_invest_customer_service
    - utter_suggest_get_info
* enter_data
    - action_check_email_n_phone
    - action_forward_customer_service
    - utter_thks_n_forward_info_to_customer_service
    - utter_anything_else

## Meey Invest 2
* how_invest_to_meeyland
    - utter_invest_customer_service
    - utter_suggest_get_info
* deny OR canthelp
    - utter_confirm
    - utter_anything_else
* deny OR canthelp
    - utter_thank

## Đăng bài 4
* greet
    - action_greet
* fee_of_vip_post
    - action_fee_of_vip_post
* user_feel_expensive
    - utter_user_feel_expensive

## Đăng bài 5
* fee_of_vip_post
    - action_fee_of_vip_post
* user_ask_price
    - action_fee_of_vip_post

## Đăng bài 6
* what_is_up_post
    - utter_what_is_up_post
* user_ask_price
    - utter_fee_of_up_post
* thank
    - utter_thank

## Đăng bài 7
* post_video_complaint
    - utter_post_video_complaint
* approval_time
    - utter_approval_time
* affirm
    - utter_anything_else
* deny
    - utter_confirm
    - utter_thank

## Đăng bài 8
* post_image_complaint
    - utter_post_image_complaint
* affirm
    - utter_anything_else
* deny
    - utter_confirm
    - utter_thank

## Đăng bài 9
* why_reject_post
    - utter_why_reject_post_1
    - utter_why_reject_post_2
    - utter_why_reject_post_3
* affirm
    - utter_anything_else
* deny
    - utter_confirm
    - utter_thank

## Đăng bài 10
* multi_content_in_a_post
    - utter_multi_content_in_a_post
* thank
    - utter_confirm
    - utter_thank

## Đăng bài 11
* limit_of_post_number
    - utter_limit_of_post_number
* thank
    - utter_thank

## Đăng bài 12
* why_reject_post
    - utter_why_reject_post_1
    - utter_why_reject_post_2
    - utter_why_reject_post_3

## Đăng bài 13
* how_create_new_post
    - utter_how_create_new_post
* request_more
    - utter_how_create_new_post_details
* request_more
    - utter_out_of_bot_ability
    - utter_how_contact_customer_service

## Đăng bài 14
* how_create_new_post
    - utter_how_create_new_post
* affirm
    - utter_confirm
    - utter_anything_else

## Đăng bài 13
* how_create_new_post
    - utter_how_create_new_post
* request_more
    - utter_how_create_new_post_details
* affirm
    - utter_confirm
    - utter_anything_else

## Câu hỏi khác 1
* how_search_info
    - action_how_to_search
* request_more OR user_need_help
    - utter_out_of_bot_ability
    - utter_how_contact_customer_service

## Câu hỏi khác 2
* error_when_download_app
    - utter_error_when_download_app
* deny
    - utter_how_contact_customer_service

## Câu hỏi khác 3
* error_when_download_app
    - utter_error_when_download_app
* error_when_download_app
    - utter_how_contact_customer_service

## Câu hỏi khác 4
* forward_to_customer_service
    - utter_forward_to_customer_service
    - utter_ask_whatspossible

## Câu hỏi khác 5
* greet
    - action_greet
* forward_to_customer_service
    - utter_forward_to_customer_service
    - utter_ask_whatspossible

## Câu hỏi khác 6
* greet
    - action_greet
* chitchat
    - respond_chitchat
* forward_to_customer_service
    - utter_forward_to_customer_service
    - utter_ask_whatspossible

## General 1
* user_need_help
    - action_greet

## General 2
* greet
    - action_greet
* affirm
    - utter_confirm

## General 3
* greet
    - action_greet
* user_need_help
    - utter_confirm

## General 4
    - utter_anything_else
* deny
    - utter_thank

## General 5
* greet
    - action_greet
* affirm
    - utter_confirm
* user_need_help
    - utter_confirm

## General 6
* greet
    - action_greet
* greet
    - action_greet
* greet
    - utter_ask_whatspossible

## General 7
* bot_need_learning OR react_negative
    - utter_keep_learning

## out_of_scope 1
* out_of_scope
    - respond_out_of_scope
    - utter_ask_whatspossible

## out_of_scope 2
* greet
    - action_greet
* out_of_scope
    - respond_out_of_scope
    - utter_ask_whatspossible

## out_of_scope 3
* greet
    - action_greet
* enter_data
    - utter_not_sure

## out_of_scope 4
* greet
    - action_greet
* chitchat
    - respond_chitchat
* out_of_scope
    - respond_out_of_scope
    - utter_ask_whatspossible

## chitchat 1
* chitchat
    - respond_chitchat
* request_more
    - utter_invest_customer_service

## chitchat 2
* chitchat
    - respond_chitchat
* how_invest_to_meeyland
    - utter_invest_customer_service
