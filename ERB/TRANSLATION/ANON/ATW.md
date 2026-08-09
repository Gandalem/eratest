![](https://lh3.googleusercontent.com/fife/AKsag4Pk-6EKlXywA4-F4dTa5vCNCKG6d8yFYBvwBc2JhsyaWUJs2q38-ygj1Q0h4-TsMjNYqt3kRvBggXGvMc7_FNh5GTH2rnU0ca6_Ue0O2Seyl6xjVC1SPpB78T1a5nna01ff2sKL0phkZgGSt4HTu4GpHbUPpa3BOd4k6LeGIVXmwvPYHn35EfuZcjMOpHRJ4a-dKZmedXk3kYMkCIxqhgUqWHyqblhIva-puUMX2R5yXGPyQGWPYOOE3WUH1Jrmy5BabTnRjBGWTndOIeHkl8RlhJwrlxctVRopxyfTCQRPljsYZ72dgR16Jyh7BLIbRpIOU4AEfOXDDlnqvrS6GOrACWQqfoB5yE3TZYKLfQ8GiKkWQFoFwCseRmFvjffeAR5CLVddcrxMw1uqGlbMAQJ4Qaui7IQv50WhhGdF7HYBNrr6VTDzUP2igYc5U2tgAQpNYaHXCMLYcI6RnOGfYQrWOAAFSShUV8ffYybg6N5UEi324RKHwMQxutIFrdGOsiNICBDn4Ya6X3xAiytf2JGikHfQf4b3t7BHUw2XWMrkOngOO3QmWtd4cTIdEq8T1S8qe4qM1Jd4cUVBkrEgPrv8IK0uIRCbJ0ZE_hySJ6nGSTMhZr3Q_OYAhHIGO4BbpX8PjAP3Xw-H5Lq6AFgYGKFROoIEI1xJLH-bwt0mQURi6P4PmQVmXruGnpXeZJvZpUABM5vGANAdgGaTse8FOVAajeEU9Cr0DfcaAyaTpszrgvvr2cwx89uf304AjygJulWY9ryyNHVqAzGp02pbsy98_MaF2ZAoEkn4uWjGLJvNQVoLpBuSIGQkXACKk3beTvxARI4Dv39QshrpgN6NqGN6zsIaeCqhp9MOdiCAqcn_X7LHeqYWB3DCWLn6B4NoWcuAVlKw7k_8CQbJPfSSwaNxOAQDrH61Wt0Y2_qWjXSMKiE2ir5M8bOJfnT1XNld0C-u8rL43P1922jaF5N4tyoRPLJWdZohA19v2GLT_ZeK4R-gKuWVyiAYO0KioDEs0_bPO2b-7Ja3o5bTnBq7LD35P9e4P18L9R2TI4VAtJWozwYZtowc-esiPY6OGAtH0sWTZNb35eO2P6t_RRtBJdRJFoqH1cFJE0oZ8zlsMkwV4z9NS2f4qhOaIusnC46tBhkv2-2cb67L9_bcSfcQNQbeGs_9YfLNaUXfqr56rXsp91zMTdYikWsl7tr3z5oGbJ_pqyOiXTDUJhC5A7tieRtt4GTpL6fQ6QddA-eMCGdNqfvmWQpxBIVbWeL0NTJr8EbAZRdtxqse47UPCi5uBCj59XOlSjyJODPauArKxmnIeHo_eCX5RYGBPYwgXJkf77VWejSXCwP42b2ZT6ih0AWszV9F5K-Vtayo9zfgCTDgeFe4ZJqkRCUdnROh5OzJ4ihSAhzeGslQQnbOeBIVcNUYEKM3P85ECK0b8fgfQYU18aQgs4CY0R8C_P1HKjEy9o-pRY27t9KQ8c-H5mixXhveWBBgJUeb1ilaGNchRGe42fY1Oo_7k98qONjVhrCUCnLjKw=w1532-h956)

AnonTW specific edits and additions go here

In no particular order:

##  HoleTight.ERB, QoL_Com_Order.ERB
- Gray out insertion commands if all checks except for hole size pass
- Show a message on what to do if you can't insert due to this reasons (ie: get [Forbidden Knowledge] or get 50 V exp as an example).

##  @NAS_DEBUG, NEWGAME.ERB, NEWGAME_MAKE.ERB, SHOP.ERB, INFO.ERB, ANON/DEBUG.ERB
- Debug menu.
- Developer quicktest.

## INFO.ERB, ATW_TOGGLES.ERB, @ALCOHOL_FACE_TR
- Global option to hide the drunk bar and sobriety if sober.

## TRANSLATION/ModularUpdate.ERB
- Added a template update menu for dialogue writers to create their update menus on.

## RAINBOW系.ERB
- Adds rainbow text, ported from eraReverse

## INFO.ERB, PRINT_STATE.ERB, 能力表示.ERB
- Used `@NOTICE_CYCLE` instead of only the menstrual cycle visualization achievement as criteria for cycle visualization.

## Too many damn files, mainly _REPLACE.CSV
- Replaced use of `\\` with the unicode `¥`, to support other fonts which render `\` properly (such as VL Gothic and whatever BBASaikou uses)

## BetterUI.ERB, PRINT_STATE.ERB, 能力表示.ERB
- Replaced the Falling Conditions tab with one that is easily expandable
- Adds the `@UniversalRank` function, used for convenience when porting between branches

## Add_Misc.ERB
- Used NPC parse for gaining Unmatched and fast recovery

## ATW_TOGGLES.ERB
- Added global option for a Spoiler Mode, makes obscure info more explicit

# RapeExpansion.ERB
- Expands the rape system by adding a new rape route and force marks.
    - If no third-party witnesses the rape, there will be no punishments except for losing the favor of the 2hu you raped
    - The victim doesn't tell anyone about the rape because of reasons (pride, gloomy personality, is ashamed of it, etc)
    - Will for the life of her try not to be alone in the same room as you from this point on
    - The victim becomes easier to rape, unlocks a rape command that you can initiate as you please, might results in her attempting to fight back.
    - FORCE marks requires Terror (a new PALAM), Submission, Depression, and Shame

# SOURCE_1.ERB
- Implemented Terror SOURCE and PALAMs. TW's fear was interpreted as a positive thing and we neeeded to make one that's more negative per se.

# COM105.ERB
- Removed blocker which doesn't allow you to put on or off rope during rape.
# SpoilerMode.ERB
- Moved item unlock requirements to `@CraftingDeny` which allows for different unlock methods other than Intimacy.
- `@CraftingDeny` is also used to track WHY you can't create an item.
- Created `@HAVE_PERMS_LIST` to store permissions for foraging, logging, and street stalls in one location
- `@HAVE_PERMS` creates a message if `@HAVE_PERMS_LIST` returns false. With the New Player Guide on, it'll tell you who you need to fall, while off, you get a vague message instead (though this time it tells you to consult with the local boss).
- `@CHARA_MAX_CUM` is the filling rate caps from the filling rate function in a separate function, used for showing the max uterus cap.

## @NOTICE_CYCLE
- Cycle visualization is now always enabled if the New Player Guide is enabled

## COM446.ERB
- Now shows a message if an item cannot be created due to not meeting crafting requirements if the New Player Guide is enabled
- Now uses `@CraftingDeny` to check if an item can be crafted due to other requirements.

## COM442.ERB, COM445.ERB, COM447.ERB
- Convert hard-coded command permissions to use the `HAVE_PERMS` system

## PREGNANCY.ERB
- Pregnancy stats are now shown if the New Player Guide is enabled.

## INFO.ERB
- Current uterus volume is now shown, if the New Player Guide is enabled, it will also show the max volume and change to yellow once it's full.
- Current date score is now shown if the New Player Guide or Show Date Scores is enabled.

## `@充填率`
- Use `@CHARA_MAX_CUM` to get the max cum a Touhou's uterus can store.

## HARDCORECONTENT.ERB
- Menu for disabling certain undesirable character events from the Japanese side, now more discriminatory

## New AL.ERB, AchievementList.ERB, GETOBJ.ERB, SHOP.ERB
- New achievement list menu
    - Has infinite scroll and allows easy showing of all achievements
    - Can show icons (no icons are currently in for now)
    - Claim visible and claim all buttons.
    - Search for achievements by typing in

- New achievement framework that is separate from the original and PedyTW system.
    - Allows for achievement names
    - Uses datatables for easy adding and sorting of achievements 
    - Claim all achievements at once or claim ones in a page