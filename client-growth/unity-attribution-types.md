---
title: Introduction to attribution
product: Unity Grow
canonical: https://docs.unity.com/en-us/grow/acquire/partner-integration/attribution/introduction
last_updated: 2026-11-18
generated_at: 2026-11-19T09:58:31.321Z
locale: en-us
---

# Introduction to attribution

> Understand Unity Ads attribution by learning how user installs are tracked through ad interactions, enabling accurate measurement of campaign performance and optimization of user acquisition strategies.

Attribution indicates whether a user installed your app after watching one of your ads and which ad network displayed the ad. This data confirms the number of installs and informs campaign models. You must pass attribution data to Unity to run a Unity Ads User Acquisition campaign.

## Attribution links

To accurately track installs and measure campaign performance, you need install postbacks called attribution links. These links verify, attribute, and timestamp app installs.

Retrieve attribution links with a [Mobile Measurement Partner (MMP)](../partner-integration-guides).

For detailed instructions on how to generate attribution links with your preferred attribution partner, refer to your MMP’s individual [Partner integration](/grow/acquire/partner-integration.md) documentation. To integrate these links with Unity in the User Acquisition dashboard, follow the instructions in [Integrate attribution links with Unity](/grow/acquire/partner-integration/attribution/integrate-links.md).

The following sections detail the data that attribution links pass to Unity.

### Attribution types

An attribution link type indicates how a user found your app. It also identifies which ad network served the ad.

Refer to the following table for descriptions of these attribution types:

| Attribution type | Description                                                              | Notes                                                                                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unity-attributed | Users install your game after watching your ad on the Unity Ads network. | -                                                                                                                                                                                        |
| Unattributed     | Users install your game after watching your ad on another ad network.    | Most MMPs don't pass unattributed data by default. The recommended best practice is to enable unattributed data because it enriches Unity's models and can improve campaign performance. |
| Organic          | Users install your game without watching an ad.                          | Unity counts organic installs as **Unattributed**.                                                                                                                                       |

### Conversion types

Attribution links can track either ad clicks or ad views that lead to installs. While only click links are required to run a User Acquisition campaign, the recommended best practice is to use both click and start (view) links because it can help to expand your campaign's reach.

Refer to the following table for descriptions of these conversion types and whether they're required with Unity:

| Conversion type | Description                                         | Required    | Notes                                   |
| --------------- | --------------------------------------------------- | ----------- | --------------------------------------- |
| Click           | Users installed your app after clicking on your ad. | Yes         | Also known as click-through attribution |
| Start           | Users installed your app after viewing your ad.     | Recommended | Also known as view-through attribution  |

When you set up attribution links with an MMP, most partners require you to define a lookback window. A lookback window is the period during which a user’s ad click or view can be credited for a resulting app install. For example, if your click-through lookback window is five days, your MMP attributes an install to an ad click if the user installs your app within five days of clicking the ad.

## App-level attribution links

If you create more than one campaign for an app, you can assign your attribution links as app-level links in the User Acquisition dashboard. App-level links automatically apply to all of your app's associated campaigns.

By integrating your attribution links as app-level links, you can create multiple campaigns without individually entering individual attribution links for each campaign. You can also edit the links for all associated campaigns by editing just the app-level link. Refer to [Integrate attribution links with Unity](/grow/acquire/partner-integration/attribution/integrate-links.md) for step-by-step instructions for creating app-level links.

> **Important:**
>
> If you set an attribution link as app-level, the campaigns associated with that app will inherit the app-level link.

## Attribution links tester

Testing your attribution links is an important step in your campaign setup and partner integration, as successful attribution is critical for correct reporting and campaign performance data.

The Attribution Links Tester is a feature of Unity's Ad Testing app, which you can download from the [Apple App Store](https://apps.apple.com/us/app/ad-testing/id1463016906) for your iOS device, or from the [Google Play Store](https://play.google.com/store/apps/details?id=com.unity3d.auicreativetestapp\&hl=en\&gl=US) for your Android device.

The recommended best practice is to test your attribution links when you generate them with your MMP. Testing your links with the Attribution Links Tester does two important things:

* Simulates a user installing the advertised game, and checks that Unity attributes the install correctly.
* Reduces your risk of failed attribution, incorrect reporting, misleading campaign performance data, and related issues.

Before you go live with a new campaign, use the Attribution Links Tester to ensure that your links are properly configured. Refer to [Test attribution links with the Ad Testing app](/grow/acquire/partner-integration/attribution/test-links.md) for detailed instructions.

## Unattributed install data

Unattributed install data is any of your app's engagement data that comes from outside of the Unity Ads network. This data is from both organic installs (when a user downloads your app organically) and installs from other ad networks.

In general, MMPs don't pass unattributed install data to Unity by default. The recommended best practice is to pass unattributed install data with your attribution links because it enriches the User Acquisition models with additional data that can improve campaign performance.

Refer to your preferred partner's integration instructions for details on how to enable passing unattributed install data to Unity:

* [AppsFlyer](/grow/acquire/partner-integration/appsflyer.md)
* [Adjust](/grow/acquire/partner-integration/adjust.md)
* [Singular](/grow/acquire/partner-integration/singular.md)
* [ByteBrew](/grow/acquire/partner-integration/bytebrew.md)
