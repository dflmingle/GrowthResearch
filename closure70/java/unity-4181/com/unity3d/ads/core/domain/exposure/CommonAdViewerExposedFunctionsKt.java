package com.unity3d.ads.core.domain.exposure;

import com.unity3d.ads.adplayer.ExposedFunction;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.repository.CampaignRepository;
import com.unity3d.ads.core.data.repository.DeviceInfoRepository;
import com.unity3d.ads.core.data.repository.SessionRepository;
import com.unity3d.ads.core.domain.AndroidGetAdPlayerContext;
import com.unity3d.ads.core.domain.CacheFile;
import com.unity3d.ads.core.domain.ExecuteAdViewerRequest;
import com.unity3d.ads.core.domain.GetIsFileCache;
import com.unity3d.ads.core.domain.HandleInvocationsFromAdViewer;
import com.unity3d.ads.core.domain.HandleOpenUrl;
import com.unity3d.ads.core.domain.Refresh;
import com.unity3d.ads.core.domain.SendDiagnosticEvent;
import com.unity3d.ads.core.domain.SendPrivacyUpdateRequest;
import com.unity3d.ads.core.domain.attribution.AndroidAttribution;
import com.unity3d.ads.core.domain.events.GetOperativeEventApi;
import com.unity3d.ads.core.domain.offerwall.GetIsOfferwallAdReady;
import com.unity3d.ads.core.domain.offerwall.LoadOfferwallAd;
import com.unity3d.ads.core.domain.om.AndroidOmInteraction;
import com.unity3d.ads.core.domain.om.GetOmData;
import com.unity3d.ads.core.domain.om.IsOMActivated;
import com.unity3d.ads.core.domain.om.OmFinishSession;
import com.unity3d.ads.core.domain.om.OmImpressionOccurred;
import com.unity3d.ads.core.domain.scar.LoadScarAd;
import com.unity3d.services.core.network.model.RequestType;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import kotlin.Metadata;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;

/* JADX INFO: compiled from: CommonAdViewerExposedFunctions.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/exposure/CommonAdViewerExposedFunctionsKt.class */
@Metadata(mv = {1, 8, 0}, k = 2, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000¾\u0001\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0012\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\f\u001a\u001b\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010\u0006\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u000b\u0010\u0007\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u000b\u0010\b\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a#\u0010\t\u001a\u00020\u00012\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u001b\u0010\u000e\u001a\u00020\u00012\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001aH\u0010\u000f\u001a\u00020\u00012\u0006\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0012\u001a\u00020\u00132\u0006\u0010\u0014\u001a\u00020\u00152\u0006\u0010\u0016\u001a\u00020\u00172\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0001ø\u0001\u0000ø\u0001\u0000¢\u0006\u0004\b\u001a\u0010\u001b\u001a\u0013\u0010\u001c\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010\u001f\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010 \u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010!\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u001b\u0010\"\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u000b\u0010#\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u0013\u0010$\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u0013\u0010%\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u0013\u0010&\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010'\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010(\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u000b\u0010)\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u0013\u0010*\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u001b\u0010+\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010,\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u0013\u0010-\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u0013\u0010.\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\u0000ø\u0001\u0000\u001a\u0013\u0010/\u001a\u00020\u00012\u0006\u00100\u001a\u000201H\u0000ø\u0001\u0000\u001a\u0013\u00102\u001a\u00020\u00012\u0006\u00103\u001a\u000204H\u0000ø\u0001\u0000\u001a\u001b\u00105\u001a\u00020\u00012\u0006\u00105\u001a\u0002062\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u00107\u001a\u00020\u00012\u0006\u00107\u001a\u0002082\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u00109\u001a\u00020\u00012\u0006\u0010:\u001a\u00020;2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010<\u001a\u00020\u00012\u0006\u0010<\u001a\u00020=2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010>\u001a\u00020\u00012\u0006\u0010?\u001a\u00020@H\u0000ø\u0001\u0000\u001a\u001b\u0010A\u001a\u00020\u00012\u0006\u0010B\u001a\u00020C2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010D\u001a\u00020\u00012\u0006\u0010D\u001a\u00020E2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010F\u001a\u00020\u00012\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010G\u001a\u00020HH\u0000ø\u0001\u0000\u001a\u000b\u0010I\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u001b\u0010J\u001a\u00020\u00012\u0006\u0010K\u001a\u00020L2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010M\u001a\u00020\u00012\u0006\u0010N\u001a\u00020O2\u0006\u0010P\u001a\u00020QH\u0000ø\u0001\u0000\u001a\u001b\u0010R\u001a\u00020\u00012\u0006\u0010R\u001a\u00020S2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u001b\u0010T\u001a\u00020\u00012\u0006\u0010U\u001a\u00020V2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010W\u001a\u00020\u00012\u0006\u0010W\u001a\u00020XH\u0000ø\u0001\u0000\u001a\u0013\u0010Y\u001a\u00020\u00012\u0006\u0010\u001d\u001a\u00020\u001eH\u0000ø\u0001\u0000\u001a\u0013\u0010Z\u001a\u00020\u00012\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010[\u001a\u00020\u00012\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010\\\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u0013\u0010]\u001a\u00020\u00012\u0006\u0010\f\u001a\u00020\rH\u0000ø\u0001\u0000\u001a\u000b\u0010^\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u000b\u0010_\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u000b\u0010`\u001a\u00020\u0001H\u0000ø\u0001\u0000\u001a\u001b\u0010a\u001a\u00020\u00012\u0006\u0010:\u001a\u00020;2\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u0013\u0010b\u001a\u00020\u00012\u0006\u0010\u0004\u001a\u00020\u0005H\u0000ø\u0001\u0000\u001a\u000b\u0010c\u001a\u00020\u0001H\u0000ø\u0001\u0000\u0082\u0002\u000b\n\u0002\b\u0019\n\u0005\b¡\u001e0\u0001¨\u0006d"}, d2 = {"attributionRegisterClick", "Lcom/unity3d/ads/adplayer/ExposedFunction;", "androidAttribution", "Lcom/unity3d/ads/core/domain/attribution/AndroidAttribution;", "adObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "attributionRegisterView", "clearStorage", "deleteStorage", "download", "cacheFile", "Lcom/unity3d/ads/core/domain/CacheFile;", "sessionRepository", "Lcom/unity3d/ads/core/data/repository/SessionRepository;", "downloadWithProgress", "getAdContext", "getAndroidAdPlayerContext", "Lcom/unity3d/ads/core/domain/AndroidGetAdPlayerContext;", HandleInvocationsFromAdViewer.KEY_AD_DATA, "Lcom/unity3d/ads/core/data/model/AdData;", HandleInvocationsFromAdViewer.KEY_IMPRESSION_CONFIG, "Lcom/unity3d/ads/core/data/model/ImpressionConfig;", HandleInvocationsFromAdViewer.KEY_AD_DATA_REFRESH_TOKEN, "Lcom/unity3d/ads/core/data/model/AdDataRefreshToken;", "isOMActivated", "Lcom/unity3d/ads/core/domain/om/IsOMActivated;", "getAdContext-yLuu4LI", "(Lcom/unity3d/ads/core/domain/AndroidGetAdPlayerContext;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Lcom/unity3d/ads/core/domain/om/IsOMActivated;Lcom/unity3d/ads/core/data/model/AdObject;)Lcom/unity3d/ads/adplayer/ExposedFunction;", "getAllowedPii", "deviceInfoRepository", "Lcom/unity3d/ads/core/data/repository/DeviceInfoRepository;", "getConnectionType", "getDeviceMaxVolume", "getDeviceVolume", "getExtra", "getKeysStorage", "getPrivacy", "getPrivacyFsm", "getScreenHeight", "getScreenWidth", "getSessionToken", "getStorage", "hbTokenIncrementStarts", "hbTokenIncrementWins", "hbTokenReset", "incrementBannerImpressionCount", "isAttributionAvailable", "isFileCached", "getIfFileCache", "Lcom/unity3d/ads/core/domain/GetIsFileCache;", "isOfferwallAdReady", "getIsOfferwallAdReady", "Lcom/unity3d/ads/core/domain/offerwall/GetIsOfferwallAdReady;", "loadOfferwallAd", "Lcom/unity3d/ads/core/domain/offerwall/LoadOfferwallAd;", "loadScarAd", "Lcom/unity3d/ads/core/domain/scar/LoadScarAd;", "markCampaignStateShown", "campaignRepository", "Lcom/unity3d/ads/core/data/repository/CampaignRepository;", "omFinishSession", "Lcom/unity3d/ads/core/domain/om/OmFinishSession;", "omGetData", "getOmData", "Lcom/unity3d/ads/core/domain/om/GetOmData;", "omImpression", "omImpressionOccurred", "Lcom/unity3d/ads/core/domain/om/OmImpressionOccurred;", "omStartSession", "Lcom/unity3d/ads/core/domain/om/AndroidOmInteraction;", "openUrl", "handleOpenUrl", "Lcom/unity3d/ads/core/domain/HandleOpenUrl;", "readStorage", "refreshAdData", "refresh", "Lcom/unity3d/ads/core/domain/Refresh;", "request", HandleInvocationsFromAdViewer.KEY_AD_TYPE, "Lcom/unity3d/services/core/network/model/RequestType;", "executeAdViewerRequest", "Lcom/unity3d/ads/core/domain/ExecuteAdViewerRequest;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "sendOperativeEvent", "getOperativeEventApi", "Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;", "sendPrivacyUpdateRequest", "Lcom/unity3d/ads/core/domain/SendPrivacyUpdateRequest;", "setAllowedPii", "setOpportunityTTL", "setOrientation", "setPrivacy", "setPrivacyFsm", "setStorage", "showOfferwallAd", "showScarAd", "updateCampaignState", "updateTrackingToken", "writeStorage", "unity-ads_defaultRelease"})
public final class CommonAdViewerExposedFunctionsKt {
    @NotNull
    /* JADX INFO: renamed from: getAdContext-yLuu4LI, reason: not valid java name */
    public static final ExposedFunction m234getAdContextyLuu4LI(@NotNull AndroidGetAdPlayerContext getAndroidAdPlayerContext, @NotNull String adData, @NotNull String impressionConfig, @NotNull String adDataRefreshToken, @NotNull IsOMActivated isOMActivated, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(getAndroidAdPlayerContext, "getAndroidAdPlayerContext");
        Intrinsics.checkNotNullParameter(adData, HandleInvocationsFromAdViewer.KEY_AD_DATA);
        Intrinsics.checkNotNullParameter(impressionConfig, HandleInvocationsFromAdViewer.KEY_IMPRESSION_CONFIG);
        Intrinsics.checkNotNullParameter(adDataRefreshToken, HandleInvocationsFromAdViewer.KEY_AD_DATA_REFRESH_TOKEN);
        Intrinsics.checkNotNullParameter(isOMActivated, "isOMActivated");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$getAdContext$1(adData, impressionConfig, adDataRefreshToken, getAndroidAdPlayerContext, adObject, isOMActivated);
    }

    @NotNull
    public static final ExposedFunction getConnectionType(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getConnectionType$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction getDeviceVolume(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getDeviceVolume$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction getDeviceMaxVolume(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getDeviceMaxVolume$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction getScreenHeight(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getScreenHeight$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction getScreenWidth(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getScreenWidth$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction openUrl(@NotNull AdObject adObject, @NotNull HandleOpenUrl handleOpenUrl) {
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        Intrinsics.checkNotNullParameter(handleOpenUrl, "handleOpenUrl");
        return new CommonAdViewerExposedFunctionsKt$openUrl$1(handleOpenUrl, adObject);
    }

    @NotNull
    public static final ExposedFunction setOrientation(@NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$setOrientation$1(adObject);
    }

    @NotNull
    public static final ExposedFunction sendOperativeEvent(@NotNull GetOperativeEventApi getOperativeEventApi, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(getOperativeEventApi, "getOperativeEventApi");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$sendOperativeEvent$1(getOperativeEventApi, adObject);
    }

    @NotNull
    public static final ExposedFunction writeStorage() {
        return CommonAdViewerExposedFunctionsKt$writeStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction readStorage() {
        return CommonAdViewerExposedFunctionsKt$readStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction deleteStorage() {
        return CommonAdViewerExposedFunctionsKt$deleteStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction clearStorage() {
        return CommonAdViewerExposedFunctionsKt$clearStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction getKeysStorage() {
        return CommonAdViewerExposedFunctionsKt$getKeysStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction getStorage() {
        return CommonAdViewerExposedFunctionsKt$getStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction setStorage() {
        return CommonAdViewerExposedFunctionsKt$setStorage$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction getPrivacyFsm(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$getPrivacyFsm$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction setPrivacyFsm(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$setPrivacyFsm$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction getPrivacy(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$getPrivacy$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction setPrivacy(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$setPrivacy$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction getAllowedPii(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$getAllowedPii$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction setAllowedPii(@NotNull DeviceInfoRepository deviceInfoRepository) {
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        return new CommonAdViewerExposedFunctionsKt$setAllowedPii$1(deviceInfoRepository);
    }

    @NotNull
    public static final ExposedFunction getSessionToken(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$getSessionToken$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction markCampaignStateShown(@NotNull CampaignRepository campaignRepository, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(campaignRepository, "campaignRepository");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$markCampaignStateShown$1(campaignRepository, adObject);
    }

    @NotNull
    public static final ExposedFunction refreshAdData(@NotNull Refresh refresh, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(refresh, "refresh");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$refreshAdData$1(refresh, adObject);
    }

    @NotNull
    public static final ExposedFunction updateTrackingToken(@NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$updateTrackingToken$1(adObject);
    }

    @NotNull
    public static final ExposedFunction sendPrivacyUpdateRequest(@NotNull SendPrivacyUpdateRequest sendPrivacyUpdateRequest) {
        Intrinsics.checkNotNullParameter(sendPrivacyUpdateRequest, "sendPrivacyUpdateRequest");
        return new CommonAdViewerExposedFunctionsKt$sendPrivacyUpdateRequest$1(sendPrivacyUpdateRequest);
    }

    @NotNull
    public static final ExposedFunction sendDiagnosticEvent(@NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$sendDiagnosticEvent$1(sendDiagnosticEvent, adObject);
    }

    @NotNull
    public static final ExposedFunction incrementBannerImpressionCount(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$incrementBannerImpressionCount$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction download(@NotNull CacheFile cacheFile, @NotNull AdObject adObject, @NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(cacheFile, "cacheFile");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$download$1(sessionRepository, cacheFile, adObject);
    }

    @NotNull
    public static final ExposedFunction downloadWithProgress(@NotNull CacheFile cacheFile, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(cacheFile, "cacheFile");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$downloadWithProgress$1(cacheFile, adObject);
    }

    @NotNull
    public static final ExposedFunction isFileCached(@NotNull GetIsFileCache getIfFileCache) {
        Intrinsics.checkNotNullParameter(getIfFileCache, "getIfFileCache");
        return new CommonAdViewerExposedFunctionsKt$isFileCached$1(getIfFileCache);
    }

    @NotNull
    public static final ExposedFunction omStartSession(@NotNull AndroidOmInteraction omStartSession, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(omStartSession, "omStartSession");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$omStartSession$1(omStartSession, adObject);
    }

    @NotNull
    public static final ExposedFunction omFinishSession(@NotNull OmFinishSession omFinishSession, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(omFinishSession, "omFinishSession");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$omFinishSession$1(omFinishSession, adObject);
    }

    @NotNull
    public static final ExposedFunction omImpression(@NotNull OmImpressionOccurred omImpressionOccurred, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(omImpressionOccurred, "omImpressionOccurred");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$omImpression$1(omImpressionOccurred, adObject);
    }

    @NotNull
    public static final ExposedFunction omGetData(@NotNull GetOmData getOmData) {
        Intrinsics.checkNotNullParameter(getOmData, "getOmData");
        return new CommonAdViewerExposedFunctionsKt$omGetData$1(getOmData);
    }

    @NotNull
    public static final ExposedFunction isAttributionAvailable(@NotNull AndroidAttribution androidAttribution) {
        Intrinsics.checkNotNullParameter(androidAttribution, "androidAttribution");
        return new CommonAdViewerExposedFunctionsKt$isAttributionAvailable$1(androidAttribution);
    }

    @NotNull
    public static final ExposedFunction attributionRegisterView(@NotNull AndroidAttribution androidAttribution, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(androidAttribution, "androidAttribution");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$attributionRegisterView$1(androidAttribution, adObject);
    }

    @NotNull
    public static final ExposedFunction attributionRegisterClick(@NotNull AndroidAttribution androidAttribution, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(androidAttribution, "androidAttribution");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$attributionRegisterClick$1(androidAttribution, adObject);
    }

    @NotNull
    public static final ExposedFunction loadScarAd(@NotNull LoadScarAd loadScarAd, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(loadScarAd, "loadScarAd");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$loadScarAd$1(adObject, loadScarAd);
    }

    @NotNull
    public static final ExposedFunction showScarAd() {
        return CommonAdViewerExposedFunctionsKt$showScarAd$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction hbTokenIncrementWins(@NotNull SessionRepository sessionRepository, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$hbTokenIncrementWins$1(adObject, sessionRepository);
    }

    @NotNull
    public static final ExposedFunction hbTokenIncrementStarts(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$hbTokenIncrementStarts$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction hbTokenReset(@NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        return new CommonAdViewerExposedFunctionsKt$hbTokenReset$1(sessionRepository);
    }

    @NotNull
    public static final ExposedFunction loadOfferwallAd(@NotNull LoadOfferwallAd loadOfferwallAd, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(loadOfferwallAd, "loadOfferwallAd");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$loadOfferwallAd$1(adObject, loadOfferwallAd);
    }

    @NotNull
    public static final ExposedFunction showOfferwallAd() {
        return CommonAdViewerExposedFunctionsKt$showOfferwallAd$1.INSTANCE;
    }

    @NotNull
    public static final ExposedFunction isOfferwallAdReady(@NotNull GetIsOfferwallAdReady getIsOfferwallAdReady) {
        Intrinsics.checkNotNullParameter(getIsOfferwallAdReady, "getIsOfferwallAdReady");
        return new CommonAdViewerExposedFunctionsKt$isOfferwallAdReady$1(getIsOfferwallAdReady);
    }

    @NotNull
    public static final ExposedFunction request(@NotNull RequestType type, @NotNull ExecuteAdViewerRequest executeAdViewerRequest) {
        Intrinsics.checkNotNullParameter(type, HandleInvocationsFromAdViewer.KEY_AD_TYPE);
        Intrinsics.checkNotNullParameter(executeAdViewerRequest, "executeAdViewerRequest");
        return new CommonAdViewerExposedFunctionsKt$request$1(executeAdViewerRequest, type);
    }

    @NotNull
    public static final ExposedFunction setOpportunityTTL(@NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$setOpportunityTTL$1(adObject);
    }

    @NotNull
    public static final ExposedFunction updateCampaignState(@NotNull CampaignRepository campaignRepository, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(campaignRepository, "campaignRepository");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$updateCampaignState$1(adObject, campaignRepository);
    }

    @NotNull
    public static final ExposedFunction getExtra(@NotNull SessionRepository sessionRepository, @NotNull AdObject adObject) {
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return new CommonAdViewerExposedFunctionsKt$getExtra$1(sessionRepository, adObject);
    }
}