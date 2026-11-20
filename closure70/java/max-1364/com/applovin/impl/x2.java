package com.applovin.impl;

import com.applovin.adview.AppLovinAdView;
import com.applovin.adview.AppLovinAdViewDisplayErrorCode;
import com.applovin.adview.AppLovinAdViewEventListener;
import com.applovin.impl.sdk.AppLovinError;
import com.applovin.impl.sdk.ad.AppLovinAdImpl;
import com.applovin.impl.sdk.nativeAd.AppLovinNativeAd;
import com.applovin.impl.sdk.nativeAd.AppLovinNativeAdEventListener;
import com.applovin.impl.sdk.nativeAd.AppLovinNativeAdLoadListener;
import com.applovin.impl.sdk.utils.CollectionUtils;
import com.applovin.mediation.MaxAd;
import com.applovin.mediation.MaxAdExpirationListener;
import com.applovin.mediation.MaxAdListener;
import com.applovin.mediation.MaxAdRequestListener;
import com.applovin.mediation.MaxAdRevenueListener;
import com.applovin.mediation.MaxAdReviewListener;
import com.applovin.mediation.MaxAdViewAdListener;
import com.applovin.mediation.MaxError;
import com.applovin.mediation.MaxReward;
import com.applovin.mediation.MaxRewardedAdListener;
import com.applovin.mediation.nativeAds.MaxNativeAdListener;
import com.applovin.mediation.nativeAds.MaxNativeAdView;
import com.applovin.sdk.AppLovinAd;
import com.applovin.sdk.AppLovinAdClickListener;
import com.applovin.sdk.AppLovinAdDisplayListener;
import com.applovin.sdk.AppLovinAdRewardListener;
import com.applovin.sdk.AppLovinAdVideoPlaybackListener;
import com.applovin.sdk.AppLovinBidTokenCollectionListener;
import com.applovin.sdk.AppLovinPostbackListener;
import com.applovin.sdk.AppLovinSdkUtils;
import java.util.Map;

/* JADX INFO: loaded from: classes.jar:com/applovin/impl/x2.class */
public abstract class x2 {
    private static boolean a = true;
    private static boolean b = true;

    public static void b(boolean z) {
        a = z;
    }

    public static void a(boolean z) {
        b = z;
    }

    public static void a(AppLovinBidTokenCollectionListener appLovinBidTokenCollectionListener, String str) {
        if (appLovinBidTokenCollectionListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinBidTokenCollectionListener.onBidTokenCollected(str);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify bid token listener about successful bid token collection", th);
                    c("onBidTokenCollected", th);
                }
            });
        }
    }

    public static void b(AppLovinBidTokenCollectionListener appLovinBidTokenCollectionListener, String str) {
        if (appLovinBidTokenCollectionListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinBidTokenCollectionListener.onBidTokenCollectionFailed(str);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify bid token listener about bid token collection failure", th);
                    c("onBidTokenCollectionFailed", th);
                }
            });
        }
    }

    public static void a(AppLovinAdDisplayListener appLovinAdDisplayListener, String str) {
        if (appLovinAdDisplayListener instanceof p2) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                ((p2) appLovinAdDisplayListener).onAdDisplayFailed(str);
            });
        }
    }

    public static void b(AppLovinAdDisplayListener appLovinAdDisplayListener, AppLovinAd appLovinAd) {
        if (appLovinAd == null || appLovinAdDisplayListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdDisplayListener.adHidden(a(appLovinAd));
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about ad being hidden", th);
                c("adHidden", th);
            }
        });
    }

    public static void a(AppLovinAdDisplayListener appLovinAdDisplayListener, AppLovinAd appLovinAd) {
        if (appLovinAd == null || appLovinAdDisplayListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdDisplayListener.adDisplayed(a(appLovinAd));
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about ad being displayed", th);
                c("adDisplayed", th);
            }
        });
    }

    public static void a(AppLovinAdClickListener appLovinAdClickListener, AppLovinAd appLovinAd) {
        if (appLovinAd == null || appLovinAdClickListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdClickListener.adClicked(a(appLovinAd));
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about ad being clicked", th);
                c("adClicked", th);
            }
        });
    }

    public static void a(AppLovinAdVideoPlaybackListener appLovinAdVideoPlaybackListener, AppLovinAd appLovinAd) {
        if (appLovinAd == null || appLovinAdVideoPlaybackListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdVideoPlaybackListener.videoPlaybackBegan(a(appLovinAd));
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about ad playback began", th);
            }
        });
    }

    public static void a(AppLovinAdVideoPlaybackListener appLovinAdVideoPlaybackListener, AppLovinAd appLovinAd, double d, boolean z) {
        if (appLovinAd == null || appLovinAdVideoPlaybackListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdVideoPlaybackListener.videoPlaybackEnded(a(appLovinAd), d, z);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about ad playback ended", th);
            }
        });
    }

    public static void a(AppLovinAdViewEventListener appLovinAdViewEventListener, AppLovinAd appLovinAd, AppLovinAdView appLovinAdView) {
        if (appLovinAd == null || appLovinAdViewEventListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdViewEventListener.adClosedFullscreen(a(appLovinAd), appLovinAdView);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about fullscreen closed event", th);
            }
        });
    }

    public static void a(AppLovinAdViewEventListener appLovinAdViewEventListener, AppLovinAd appLovinAd, AppLovinAdView appLovinAdView, AppLovinAdViewDisplayErrorCode appLovinAdViewDisplayErrorCode) {
        if (appLovinAd == null || appLovinAdViewEventListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdViewEventListener.adFailedToDisplay(a(appLovinAd), appLovinAdView, appLovinAdViewDisplayErrorCode);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about display failed event", th);
            }
        });
    }

    public static void f(MaxAdListener maxAdListener, MaxAd maxAd) {
        f(maxAdListener, maxAd, false);
    }

    public static void e(MaxAdListener maxAdListener, MaxAd maxAd) {
        e(maxAdListener, maxAd, false);
    }

    public static void a(AppLovinAdRewardListener appLovinAdRewardListener, AppLovinAd appLovinAd, Map map) {
        if (appLovinAd == null || appLovinAdRewardListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdRewardListener.userRewardRejected(a(appLovinAd), map);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad reward listener about reward validation request being rejected", th);
            }
        });
    }

    public static void f(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdLoaded(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdLoaded", th, z);
                    b("maxAdLoaded", th, z);
                    return;
                }
            }
            maxAdListener.onAdLoaded(maxAd);
        });
    }

    public static void e(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdHidden(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdHidden", th, z);
                    b("maxAdHidden", th, z);
                    return;
                }
            }
            maxAdListener.onAdHidden(maxAd);
        });
    }

    public static void c(AppLovinAdViewEventListener appLovinAdViewEventListener, AppLovinAd appLovinAd, AppLovinAdView appLovinAdView) {
        if (appLovinAd == null || appLovinAdViewEventListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdViewEventListener.adOpenedFullscreen(a(appLovinAd), appLovinAdView);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about fullscreen opened event", th);
            }
        });
    }

    public static void a(AppLovinAdRewardListener appLovinAdRewardListener, AppLovinAd appLovinAd, int i) {
        if (appLovinAd == null || appLovinAdRewardListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdRewardListener.validationRequestFailed(a(appLovinAd), i);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad reward listener about reward validation request failing", th);
            }
        });
    }

    public static void c(AppLovinAdRewardListener appLovinAdRewardListener, AppLovinAd appLovinAd, Map map) {
        if (appLovinAd == null || appLovinAdRewardListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdRewardListener.userRewardVerified(a(appLovinAd), map);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad reward listener about successful reward validation request", th);
            }
        });
    }

    public static void a(MaxAdListener maxAdListener, String str, MaxError maxError) {
        a(maxAdListener, str, maxError, false);
    }

    public static void a(MaxAdListener maxAdListener, String str, MaxError maxError, boolean z) {
        if (str == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdLoadFailed(str, maxError);
                    return;
                } catch (Throwable th) {
                    a("onAdLoadFailed", th, z);
                    b("maxAdLoadFailed", th, z);
                    return;
                }
            }
            maxAdListener.onAdLoadFailed(str, maxError);
        });
    }

    public static void c(MaxAdListener maxAdListener, MaxAd maxAd) {
        c(maxAdListener, maxAd, false);
    }

    public static void c(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdDisplayed(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdDisplayed", th, z);
                    b("maxAdDisplayed", th, z);
                    return;
                }
            }
            maxAdListener.onAdDisplayed(maxAd);
        });
    }

    public static void b(AppLovinAdViewEventListener appLovinAdViewEventListener, AppLovinAd appLovinAd, AppLovinAdView appLovinAdView) {
        if (appLovinAd == null || appLovinAdViewEventListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdViewEventListener.adLeftApplication(a(appLovinAd), appLovinAdView);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad event listener about application leave event", th);
            }
        });
    }

    public static void d(MaxAdListener maxAdListener, MaxAd maxAd) {
        d(maxAdListener, maxAd, false);
    }

    public static void d(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || !(maxAdListener instanceof MaxAdViewAdListener)) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    ((MaxAdViewAdListener) maxAdListener).onAdExpanded(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdExpanded", th, z);
                    b("maxAdExpanded", th, z);
                    return;
                }
            }
            ((MaxAdViewAdListener) maxAdListener).onAdExpanded(maxAd);
        });
    }

    public static void b(AppLovinAdRewardListener appLovinAdRewardListener, AppLovinAd appLovinAd, Map map) {
        if (appLovinAd == null || appLovinAdRewardListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(() -> {
            try {
                appLovinAdRewardListener.userOverQuota(a(appLovinAd), map);
            } catch (Throwable th) {
                com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify ad reward listener about exceeding quota", th);
            }
        });
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd) {
        a(maxAdListener, maxAd, false);
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdClicked(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdClicked", th, z);
                    b("maxAdClicked", th, z);
                    return;
                }
            }
            maxAdListener.onAdClicked(maxAd);
        });
    }

    public static void b(MaxAdListener maxAdListener, MaxAd maxAd) {
        b(maxAdListener, maxAd, false);
    }

    private static boolean c(boolean z) {
        return z ? a : b;
    }

    public static void b(MaxAdListener maxAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || !(maxAdListener instanceof MaxAdViewAdListener)) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    ((MaxAdViewAdListener) maxAdListener).onAdCollapsed(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdCollapsed", th, z);
                    b("maxAdCollapsed", th, z);
                    return;
                }
            }
            ((MaxAdViewAdListener) maxAdListener).onAdCollapsed(maxAd);
        });
    }

    private static void c(String str, Throwable th) {
        com.applovin.impl.sdk.l lVar = com.applovin.impl.sdk.l.F0;
        if (lVar != null) {
            lVar.E().c("ListenerCallbackInvoker", str, th);
        }
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd, MaxError maxError) {
        a(maxAdListener, maxAd, maxError, false);
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd, MaxError maxError, boolean z) {
        if (maxAd == null || maxAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdListener.onAdDisplayFailed(maxAd, maxError);
                    return;
                } catch (Throwable th) {
                    a("onAdDisplayFailed", th, z);
                    b("maxAdDisplayFailed", th, z);
                    return;
                }
            }
            maxAdListener.onAdDisplayFailed(maxAd, maxError);
        });
    }

    public static void b(MaxNativeAdListener maxNativeAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxNativeAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxNativeAdListener.onNativeAdExpired(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onNativeAdExpired", th, z);
                    b("maxNativeAdExpired", th, z);
                    return;
                }
            }
            maxNativeAdListener.onNativeAdExpired(maxAd);
        });
    }

    public static void a(MaxAdRevenueListener maxAdRevenueListener, MaxAd maxAd) {
        a(maxAdRevenueListener, maxAd, false);
    }

    public static void a(MaxAdRevenueListener maxAdRevenueListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxAdRevenueListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdRevenueListener.onAdRevenuePaid(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onAdRevenuePaid", th, z);
                    b("maxAdPaidRevenue", th, z);
                    return;
                }
            }
            maxAdRevenueListener.onAdRevenuePaid(maxAd);
        });
    }

    public static void b(AppLovinNativeAdLoadListener appLovinNativeAdLoadListener, AppLovinError appLovinError) {
        if (appLovinNativeAdLoadListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinNativeAdLoadListener.onNativeAdLoadFailed(appLovinError);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify native ad event listener about ad failing to load", th);
                    c("nativeAdLoadFailed", th);
                }
            });
        }
    }

    public static void b(AppLovinNativeAdEventListener appLovinNativeAdEventListener, AppLovinNativeAd appLovinNativeAd) {
        if (appLovinNativeAdEventListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinNativeAdEventListener.onNativeAdClicked(appLovinNativeAd);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify native ad event listener about ad click", th);
                    c("nativeAdClicked", th);
                }
            });
        }
    }

    public static void b(MaxAdReviewListener maxAdReviewListener, String str, MaxAd maxAd) {
        a(maxAdReviewListener, str, maxAd, false);
    }

    private static void b(String str, Throwable th) {
        com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Error in publisher callback '" + str + "'", th);
    }

    private static void b(String str, Throwable th, boolean z) {
        if (com.applovin.impl.sdk.l.F0 != null) {
            com.applovin.impl.sdk.l.F0.E().a("ListenerCallbackInvoker", str, th, CollectionUtils.hashMap("details", "isPublisherCallback=" + z));
        }
    }

    public static void a(MaxAdRequestListener maxAdRequestListener, String str) {
        a(maxAdRequestListener, str, false);
    }

    public static void a(MaxAdRequestListener maxAdRequestListener, String str, boolean z) {
        if (str == null || maxAdRequestListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdRequestListener.onAdRequestStarted(str);
                    return;
                } catch (Throwable th) {
                    a("onAdRequestStarted", th, z);
                    b("maxAdRequestStarted", th, z);
                    return;
                }
            }
            maxAdRequestListener.onAdRequestStarted(str);
        });
    }

    public static void a(MaxAdExpirationListener maxAdExpirationListener, MaxAd maxAd, MaxAd maxAd2, boolean z) {
        if (maxAd == null || maxAd2 == null || maxAdExpirationListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxAdExpirationListener.onExpiredAdReloaded(maxAd, maxAd2);
                    return;
                } catch (Throwable th) {
                    a("onExpiredAdReloaded", th, z);
                    b("maxExpiredAdReloaded", th, z);
                    return;
                }
            }
            maxAdExpirationListener.onExpiredAdReloaded(maxAd, maxAd2);
        });
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd, MaxReward maxReward) {
        a(maxAdListener, maxAd, maxReward, false);
    }

    public static void a(MaxAdListener maxAdListener, MaxAd maxAd, MaxReward maxReward, boolean z) {
        if (maxAd == null || !(maxAdListener instanceof MaxRewardedAdListener)) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    ((MaxRewardedAdListener) maxAdListener).onUserRewarded(maxAd, maxReward);
                    return;
                } catch (Throwable th) {
                    a("onUserRewarded", th, z);
                    b("maxRewardedUser", th, z);
                    return;
                }
            }
            ((MaxRewardedAdListener) maxAdListener).onUserRewarded(maxAd, maxReward);
        });
    }

    public static void a(MaxNativeAdListener maxNativeAdListener, MaxNativeAdView maxNativeAdView, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxNativeAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxNativeAdListener.onNativeAdLoaded(maxNativeAdView, maxAd);
                    return;
                } catch (Throwable th) {
                    a("onNativeAdLoaded", th, z);
                    b("maxNativeAdLoaded", th, z);
                    return;
                }
            }
            maxNativeAdListener.onNativeAdLoaded(maxNativeAdView, maxAd);
        });
    }

    public static void a(MaxNativeAdListener maxNativeAdListener, String str, MaxError maxError, boolean z) {
        if (str == null || maxNativeAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxNativeAdListener.onNativeAdLoadFailed(str, maxError);
                    return;
                } catch (Throwable th) {
                    a("onNativeAdLoadFailed", th, z);
                    b("maxNativeAdLoadFailed", th, z);
                    return;
                }
            }
            maxNativeAdListener.onNativeAdLoadFailed(str, maxError);
        });
    }

    public static void a(MaxNativeAdListener maxNativeAdListener, MaxAd maxAd, boolean z) {
        if (maxAd == null || maxNativeAdListener == null) {
            return;
        }
        AppLovinSdkUtils.runOnUiThread(z, () -> {
            if (c(z)) {
                try {
                    maxNativeAdListener.onNativeAdClicked(maxAd);
                    return;
                } catch (Throwable th) {
                    a("onNativeAdClicked", th, z);
                    b("maxNativeAdClicked", th, z);
                    return;
                }
            }
            maxNativeAdListener.onNativeAdClicked(maxAd);
        });
    }

    public static void a(AppLovinPostbackListener appLovinPostbackListener, String str) {
        if (appLovinPostbackListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinPostbackListener.onPostbackSuccess(str);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify AppLovinPostbackListener about postback URL (" + str + ") executed", th);
                }
            });
        }
    }

    public static void a(AppLovinPostbackListener appLovinPostbackListener, String str, int i) {
        if (appLovinPostbackListener != null) {
            AppLovinSdkUtils.runOnUiThread(() -> {
                try {
                    appLovinPostbackListener.onPostbackFailure(str, i);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify AppLovinPostbackListener about postback URL (" + str + ") failing to execute with error code (" + i + "):", th);
                }
            });
        }
    }

    public static void a(MaxAdReviewListener maxAdReviewListener, String str, MaxAd maxAd, boolean z) {
        if (maxAdReviewListener != null) {
            AppLovinSdkUtils.runOnUiThread(z, () -> {
                try {
                    maxAdReviewListener.onCreativeIdGenerated(str, maxAd);
                } catch (Throwable th) {
                    com.applovin.impl.sdk.p.c("ListenerCallbackInvoker", "Unable to notify Ad Review creative id generated", th);
                    c("adReviewCreativeIdGenerated", th);
                }
            });
        }
    }

    private static AppLovinAd a(AppLovinAd appLovinAd) {
        AppLovinAdImpl appLovinAdImpl = (AppLovinAdImpl) appLovinAd;
        return appLovinAdImpl.getDummyAd() != null ? appLovinAdImpl.getDummyAd() : appLovinAd;
    }

    private static void a(String str, Throwable th, boolean z) {
        if (z) {
            b(str, th);
        } else {
            a(str, th);
        }
    }

    private static void a(String str, Throwable th) {
        com.applovin.impl.sdk.p.b("ListenerCallbackInvoker", "Error in internal callback '" + str + "'", th);
    }
}