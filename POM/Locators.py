### Common PAGE
page_ID = {
    'scrollableRecyclerView': 'android:id/list',
}

page_XPATH = {
    'postsGrid': "//android.widget.Button[contains(@content-desc, 'Row 1, Column 1')]",
}

### HOME PAGE
homePage_ID = {
    'storiesCommon': 'com.instagram.android:id/avatar_image_view',
    'newPosts_PillButton': 'com.instagram.android:id/new_feed_pill'
}

### Ribbon
ribbon_XPath = {
    'bottomBar_homeButton': "//android.widget.FrameLayout[@content-desc='Home']/android.view.ViewGroup/android.widget.FrameLayout/android.widget.ImageView",
    'topBar_homeButton': "//android.widget.Button[@content-desc='Scroll to top']",
    'bottomBar_Search': "//android.widget.FrameLayout[@content-desc='Search and explore']",
    'bottomBar_OwnProfile': "//android.widget.Button[@content-desc='Profile']/android.view.ViewGroup",
    'activity': "//android.widget.Button[@content-desc='Activity']",
    'message': "//android.widget.Button[@content-desc='Message']",
}

ribbon_ID = {
    'backButton': 'com.instagram.android:id/action_bar_button_back',
    'bottomBar_OwnProfile': 'com.instagram.android:id/tab_avatar',
    'bottomBar_searchPage': 'com.instagram.android:id/search_tab'
}

### USER PAGE
userPage_ID = {
    'followersWindow': 'com.instagram.android:id/row_profile_header_textview_followers_count',
    'followingWindow': 'com.instagram.android:id/row_profile_header_textview_following_count',
    'followingHashTagWindow': 'com.instagram.android:id/row_hashtag_link_title',
    'followingSearchField': 'com.instagram.android:id/row_search_edit_text',
    'followingSearchResult': 'com.instagram.android:id/follow_list_username',
    'followingSortingButton': 'com.instagram.android:id/sorting_entry_row_icon',
    'followingHashTagSearchResult': 'com.instagram.android:id/follow_list_username',
    'postsCount': "com.instagram.android:id/row_profile_header_textview_post_count",
    'userName': 'com.instagram.android:id/action_bar_title',
    'altName': 'com.instagram.android:id/profile_header_full_name',
    'bio': 'com.instagram.android:id/profile_header_bio_text',
    'EmptyProfileNotice': 'com.instagram.android:id/row_profile_header_empty_profile_notice_title',
    'UnfollowSecond': 'com.instagram.android:id/follow_sheet_unfollow_row',
    'UnfollowFinal': 'com.instagram.android:id/primary_button',
    'MuteButton': 'com.instagram.android:id/follow_sheet_mute_row',
    'MutePosts': 'com.instagram.android:id/posts_mute_setting_row_switch',
    'MuteStories': 'com.instagram.android:id/stories_mute_setting_row_switch',
}

userPage_XPATH = {
    'Button_Following': "//android.widget.Button[contains(@content-desc,'Following')]",
    'Button_Follow': "//android.widget.Button[contains(@content-desc,'Follow')]",
    'Button_FollowBack': "//android.widget.Button[contains(@content-desc,'back')]",
    'Button_Requested': "//android.widget.Button[contains(@content-desc,'Requested')]",
    'following_sorting_option_latest': "//android.widget.TextView[contains(@text,'Latest')]/..//android.widget.RadioButton",
    'following_sorting_option_earliest': "//android.widget.TextView[contains(@text,'Earliest')]/..//android.widget.RadioButton",
    'following_sorting_option_default': "//android.widget.TextView[contains(@text,'Default')]/..//android.widget.RadioButton",
}
### SEARCH PAGE
searchPage_ID = {
    'searchBarField': 'com.instagram.android:id/action_bar_search_edit_text',
    'resultsCommon_Users': 'com.instagram.android:id/row_search_user_username',
    'resultsCommon_Tags': 'com.instagram.android:id/row_hashtag_textview_tag_name',
}

### HASHTAG PAGE
hashTagPage_Xpath = {
    'recent': "//android.widget.TextView[@content-desc='Recent']",
    'filterButton': "//android.widget.TextView[@content-desc='Recent']",
    'top': "//android.widget.TextView[@content-desc='Top']",
    'count_desktop_browser': "//*[@class='g47SY ']"
}

hashTagPage_ID = {
    'postsCommon': 'com.instagram.android:id/image_button',
    'hashTag': 'com.instagram.android:id/action_bar_title',
}

### POST
post_ID = {
    "header": 'com.instagram.android:id/row_feed_profile_header',
    "pic": 'com.instagram.android:id/zoomable_view_container',
    "buttonRow": "com.instagram.android:id/row_feed_view_group_buttons",
    "like": "com.instagram.android:id/row_feed_button_like",
    "comment": "com.instagram.android:id/row_feed_button_comment",
    "commentExpanded": "com.instagram.android:id/row_comment_textview_comment",
    "save": "com.instagram.android:id/row_feed_button_save",
    "likes": "com.instagram.android:id/like_row",
    "usersLiked_Common": "com.instagram.android:id/row_user_primary_name",
    "postingUser": 'com.instagram.android:id/row_feed_photo_profile_name',
    "location": 'com.instagram.android:id/secondary_label',
    "advertLink": 'com.instagram.android:id/row_feed_cta',
    "advertClose": 'com.instagram.android:id/ig_browser_close_button',
    "imageCarousel": 'com.instagram.android:id/carousel_media_group',
    "userAvatar": 'com.instagram.android:id/row_feed_photo_profile_imageview',
    "backButton": 'com.instagram.android:id/action_bar_button_back',
}

post_XPATH = {
    'firstComment': '//com.instagram.ui.widget.textview.IgTextLayoutView//android.view.View[@content-desc]',
}
