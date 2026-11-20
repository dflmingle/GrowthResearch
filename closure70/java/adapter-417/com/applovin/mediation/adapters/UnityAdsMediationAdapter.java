package com.applovin.mediation.adapters;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import androidx.annotation.Nullable;
import com.applovin.mediation.MaxAdFormat;
import com.applovin.mediation.adapter.MaxAdViewAdapter;
import com.applovin.mediation.adapter.MaxAdapter$InitializationStatus;
import com.applovin.mediation.adapter.MaxAdapter$OnCompletionListener;
import com.applovin.mediation.adapter.MaxAdapterError;
import com.applovin.mediation.adapter.MaxInterstitialAdapter;
import com.applovin.mediation.adapter.MaxRewardedAdapter;
import com.applovin.mediation.adapter.MaxSignalProvider;
import com.applovin.mediation.adapter.listeners.MaxAdViewAdapterListener;
import com.applovin.mediation.adapter.listeners.MaxInterstitialAdapterListener;
import com.applovin.mediation.adapter.listeners.MaxRewardedAdapterListener;
import com.applovin.mediation.adapter.listeners.MaxSignalCollectionListener;
import com.applovin.mediation.adapter.parameters.MaxAdapterInitializationParameters;
import com.applovin.mediation.adapter.parameters.MaxAdapterParameters;
import com.applovin.mediation.adapter.parameters.MaxAdapterResponseParameters;
import com.applovin.mediation.adapter.parameters.MaxAdapterSignalCollectionParameters;
import com.applovin.mediation.adapters.unityads.BuildConfig;
import com.applovin.sdk.AppLovinSdk;
import com.applovin.sdk.AppLovinSdkUtils;
import com.unity3d.ads.AdFormat;
import com.unity3d.ads.TokenConfiguration;
import com.unity3d.ads.UnityAds;
import com.unity3d.ads.UnityAds$UnityAdsLoadError;
import com.unity3d.ads.UnityAds$UnityAdsShowError;
import com.unity3d.ads.UnityAdsLoadOptions;
import com.unity3d.ads.UnityAdsShowOptions;
import com.unity3d.ads.metadata.MediationMetaData;
import com.unity3d.ads.metadata.MetaData;
import com.unity3d.services.banners.BannerErrorCode;
import com.unity3d.services.banners.BannerErrorInfo;
import com.unity3d.services.banners.BannerView;
import com.unity3d.services.banners.UnityBannerSize;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/* JADX INFO: loaded from: classes.jar:com/applovin/mediation/adapters/UnityAdsMediationAdapter.class */
public class UnityAdsMediationAdapter extends MediationAdapterBase implements MaxSignalProvider, MaxInterstitialAdapter, MaxRewardedAdapter, MaxAdViewAdapter {
    private static final AtomicBoolean initialized = new AtomicBoolean();
    private static MaxAdapter$InitializationStatus initializationStatus;
    private String biddingAdId;
    private BannerView bannerView;

    static /* synthetic */ MaxAdapter$InitializationStatus access$002(MaxAdapter$InitializationStatus x0) {
        initializationStatus = x0;
        return x0;
    }

    static /* synthetic */ MaxAdapterError access$100(UnityAds$UnityAdsLoadError x0, String x1) {
        return toMaxError(x0, x1);
    }

    static /* synthetic */ MaxAdapterError access$200(BannerErrorInfo x0) {
        return toMaxError(x0);
    }

    public UnityAdsMediationAdapter(AppLovinSdk sdk) {
        super(sdk);
    }

    public void initialize(MaxAdapterInitializationParameters parameters, @Nullable Activity activity, MaxAdapter$OnCompletionListener onCompletionListener) {
        Context context = getContext(activity);
        updatePrivacyConsent(parameters, context);
        if (initialized.compareAndSet(false, true)) {
            Bundle serverParameters = parameters.getServerParameters();
            String gameId = serverParameters.getString("game_id", null);
            log("Initializing UnityAds SDK with game id: " + gameId + "...");
            initializationStatus = MaxAdapter$InitializationStatus.INITIALIZING;
            MediationMetaData mediationMetaData = new MediationMetaData(context);
            mediationMetaData.setName("MAX");
            mediationMetaData.setVersion(AppLovinSdk.VERSION);
            mediationMetaData.set("adapter_version", getAdapterVersion());
            mediationMetaData.commit();
            UnityAds.setDebugMode(parameters.isTesting());
            UnityAds.initialize(context, gameId, parameters.isTesting(), new UnityAdsMediationAdapter$1(this, onCompletionListener));
            return;
        }
        onCompletionListener.onCompletion(initializationStatus, (String) null);
    }

    public String getSdkVersion() {
        return UnityAds.getVersion();
    }

    public String getAdapterVersion() {
        return BuildConfig.VERSION_NAME;
    }

    public void onDestroy() {
        if (this.bannerView != null) {
            this.bannerView.destroy();
            this.bannerView = null;
        }
    }

    public void collectSignal(MaxAdapterSignalCollectionParameters parameters, @Nullable Activity activity, MaxSignalCollectionListener callback) {
        log("Collecting signal...");
        updatePrivacyConsent(parameters, getContext(activity));
        AdFormat unityFormat = toUnityAdFormat(parameters);
        UnityAds.getToken(new TokenConfiguration(unityFormat), token -> {
            log("Collected signal");
            callback.onSignalCollected(token);
        });
    }

    public void loadInterstitialAd(MaxAdapterResponseParameters parameters, @Nullable Activity activity, MaxInterstitialAdapterListener listener) {
        String placementId = parameters.getThirdPartyAdPlacementId();
        log("Loading " + (AppLovinSdkUtils.isValidString(parameters.getBidResponse()) ? "bidding " : "") + "interstitial ad for placement \"" + placementId + "\"...");
        updatePrivacyConsent(parameters, getContext(activity));
        this.biddingAdId = UUID.randomUUID().toString();
        UnityAds.load(placementId, createAdLoadOptions(parameters), new UnityAdsMediationAdapter$2(this, listener));
    }

    public void showInterstitialAd(MaxAdapterResponseParameters parameters, @Nullable Activity activity, MaxInterstitialAdapterListener listener) {
        String placementId = parameters.getThirdPartyAdPlacementId();
        log("Showing interstitial ad for placement \"" + placementId + "\"...");
        UnityAds.show(activity, placementId, createAdShowOptions(), new UnityAdsMediationAdapter$3(this, listener));
    }

    public void loadRewardedAd(MaxAdapterResponseParameters parameters, @Nullable Activity activity, MaxRewardedAdapterListener listener) {
        String placementId = parameters.getThirdPartyAdPlacementId();
        log("Loading " + (AppLovinSdkUtils.isValidString(parameters.getBidResponse()) ? "bidding " : "") + "rewarded ad for placement \"" + placementId + "\"...");
        updatePrivacyConsent(parameters, getContext(activity));
        this.biddingAdId = UUID.randomUUID().toString();
        UnityAds.load(placementId, createAdLoadOptions(parameters), new UnityAdsMediationAdapter$4(this, listener));
    }

    public void showRewardedAd(MaxAdapterResponseParameters parameters, @Nullable Activity activity, MaxRewardedAdapterListener listener) {
        String placementId = parameters.getThirdPartyAdPlacementId();
        log("Showing rewarded ad for placement \"" + placementId + "\"...");
        configureReward(parameters);
        UnityAds.show(activity, placementId, createAdShowOptions(), new UnityAdsMediationAdapter$5(this, listener));
    }

    public void loadAdViewAd(MaxAdapterResponseParameters parameters, MaxAdFormat adFormat, @Nullable Activity activity, MaxAdViewAdapterListener listener) {
        String placementId = parameters.getThirdPartyAdPlacementId();
        log("Loading " + (AppLovinSdkUtils.isValidString(parameters.getBidResponse()) ? "bidding " : "") + adFormat.getLabel() + " ad for placement \"" + placementId + "\"...");
        if (activity == null) {
            log(adFormat.getLabel() + " ad placement \"" + placementId + "\" load failed: Activity is null");
            MaxAdapterError error = MaxAdapterError.MISSING_ACTIVITY;
            listener.onAdViewAdLoadFailed(error);
        } else {
            updatePrivacyConsent(parameters, getContext(activity));
            this.biddingAdId = UUID.randomUUID().toString();
            this.bannerView = new BannerView(activity, placementId, toUnityBannerSize(adFormat));
            this.bannerView.setListener(new UnityAdsMediationAdapter$6(this, adFormat, placementId, listener));
            this.bannerView.load(createAdLoadOptions(parameters));
        }
    }

    private UnityAdsLoadOptions createAdLoadOptions(MaxAdapterResponseParameters parameters) {
        UnityAdsLoadOptions options = new UnityAdsLoadOptions();
        String bidResponse = parameters.getBidResponse();
        if (AppLovinSdkUtils.isValidString(bidResponse)) {
            options.setAdMarkup(bidResponse);
        }
        if (AppLovinSdkUtils.isValidString(this.biddingAdId)) {
            options.setObjectId(this.biddingAdId);
        }
        return options;
    }

    private UnityAdsShowOptions createAdShowOptions() {
        UnityAdsShowOptions options = new UnityAdsShowOptions();
        if (AppLovinSdkUtils.isValidString(this.biddingAdId)) {
            options.setObjectId(this.biddingAdId);
        }
        return options;
    }

    private AdFormat toUnityAdFormat(MaxAdapterSignalCollectionParameters parameters) {
        MaxAdFormat adFormat = parameters.getAdFormat();
        if (adFormat.isAdViewAd()) {
            return AdFormat.BANNER;
        }
        if (adFormat == MaxAdFormat.INTERSTITIAL) {
            return AdFormat.INTERSTITIAL;
        }
        if (adFormat == MaxAdFormat.REWARDED) {
            return AdFormat.REWARDED;
        }
        throw new IllegalArgumentException("Unsupported ad format: " + adFormat);
    }

    private UnityBannerSize toUnityBannerSize(MaxAdFormat adFormat) {
        if (adFormat == MaxAdFormat.BANNER) {
            return new UnityBannerSize(320, 50);
        }
        if (adFormat == MaxAdFormat.LEADER) {
            return new UnityBannerSize(728, 90);
        }
        if (adFormat == MaxAdFormat.MREC) {
            return new UnityBannerSize(300, 250);
        }
        throw new IllegalArgumentException("Unsupported ad format: " + adFormat);
    }

    private static MaxAdapterError toMaxError(BannerErrorInfo unityAdsBannerError) {
        MaxAdapterError adapterError;
        if (unityAdsBannerError.errorCode == BannerErrorCode.NO_FILL) {
            adapterError = MaxAdapterError.NO_FILL;
        } else if (unityAdsBannerError.errorCode == BannerErrorCode.NATIVE_ERROR) {
            adapterError = MaxAdapterError.INTERNAL_ERROR;
        } else if (unityAdsBannerError.errorCode == BannerErrorCode.WEBVIEW_ERROR) {
            adapterError = MaxAdapterError.WEBVIEW_ERROR;
        } else {
            adapterError = MaxAdapterError.UNSPECIFIED;
        }
        return new MaxAdapterError(adapterError, unityAdsBannerError.errorCode.ordinal(), unityAdsBannerError.errorMessage);
    }

    private static MaxAdapterError toMaxError(UnityAds$UnityAdsLoadError loadError, String errorMessage) {
        MaxAdapterError adapterError = MaxAdapterError.UNSPECIFIED;
        switch (UnityAdsMediationAdapter$7.$SwitchMap$com$unity3d$ads$UnityAds$UnityAdsLoadError[loadError.ordinal()]) {
            case 1:
                adapterError = MaxAdapterError.NOT_INITIALIZED;
                break;
            case 2:
                adapterError = MaxAdapterError.INTERNAL_ERROR;
                break;
            case 3:
                adapterError = MaxAdapterError.INVALID_CONFIGURATION;
                break;
            case 4:
                adapterError = MaxAdapterError.NO_FILL;
                break;
            case 5:
                adapterError = MaxAdapterError.TIMEOUT;
                break;
        }
        return new MaxAdapterError(adapterError, loadError.ordinal(), errorMessage);
    }

    private static MaxAdapterError toMaxError(UnityAds$UnityAdsShowError showError, String errorMessage) {
        MaxAdapterError adapterError = MaxAdapterError.UNSPECIFIED;
        switch (UnityAdsMediationAdapter$7.$SwitchMap$com$unity3d$ads$UnityAds$UnityAdsShowError[showError.ordinal()]) {
            case 1:
                adapterError = MaxAdapterError.NOT_INITIALIZED;
                break;
            case 2:
                adapterError = MaxAdapterError.AD_NOT_READY;
                break;
            case 3:
                adapterError = MaxAdapterError.WEBVIEW_ERROR;
                break;
            case 4:
                adapterError = MaxAdapterError.INVALID_CONFIGURATION;
                break;
            case 5:
                adapterError = MaxAdapterError.NO_CONNECTION;
                break;
            case 6:
                adapterError = MaxAdapterError.INVALID_LOAD_STATE;
                break;
            case 7:
                adapterError = MaxAdapterError.INTERNAL_ERROR;
                break;
        }
        return new MaxAdapterError(adapterError, showError.ordinal(), errorMessage);
    }

    private void updatePrivacyConsent(MaxAdapterParameters parameters, Context context) {
        MetaData privacyMetaData = new MetaData(context);
        Boolean hasUserConsent = parameters.hasUserConsent();
        if (hasUserConsent != null) {
            privacyMetaData.set("gdpr.consent", hasUserConsent);
            privacyMetaData.commit();
        }
        Boolean isDoNotSell = parameters.isDoNotSell();
        if (isDoNotSell != null) {
            privacyMetaData.set("privacy.consent", Boolean.valueOf(!isDoNotSell.booleanValue()));
            privacyMetaData.commit();
        }
        privacyMetaData.set("privacy.mode", "mixed");
        privacyMetaData.commit();
    }

    private Context getContext(@Nullable Activity activity) {
        return activity != null ? activity.getApplicationContext() : getApplicationContext();
    }
}