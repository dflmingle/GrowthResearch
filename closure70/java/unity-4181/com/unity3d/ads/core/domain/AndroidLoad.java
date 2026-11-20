package com.unity3d.ads.core.domain;

import android.content.Context;
import com.google.protobuf.ByteString;
import com.unity3d.ads.UnityAdsErrorKt;
import com.unity3d.ads.UnityAdsLoadOptions;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.model.Failure;
import com.unity3d.ads.core.data.model.LoadResult;
import com.unity3d.ads.core.data.model.exception.GatewayException;
import com.unity3d.ads.core.data.model.exception.NetworkTimeoutException;
import com.unity3d.ads.core.data.model.exception.UnityAdsNetworkException;
import com.unity3d.ads.core.data.repository.AdRepository;
import com.unity3d.ads.core.data.repository.SessionRepository;
import com.unity3d.ads.gatewayclient.GatewayClient;
import gatewayprotocol.v1.AdRequestOuterClass$BannerSize;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticAdType;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.ErrorOuterClass$PublicErrorCode;
import gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup;
import kotlin.Metadata;
import kotlin.coroutines.Continuation;
import kotlin.jvm.internal.Intrinsics;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineDispatcher;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/* JADX INFO: compiled from: AndroidLoad.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/AndroidLoad.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000\u009a\u0001\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\b\u0000\u0018\u00002\u00020\u0001BU\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\t\u0012\u0006\u0010\n\u001a\u00020\u000b\u0012\u0006\u0010\f\u001a\u00020\r\u0012\u0006\u0010\u000e\u001a\u00020\u000f\u0012\u0006\u0010\u0010\u001a\u00020\u0011\u0012\u0006\u0010\u0012\u001a\u00020\u0013\u0012\u0006\u0010\u0014\u001a\u00020\u0015¢\u0006\u0002\u0010\u0016J0\u0010\u0017\u001a\u00020\u00182\u0006\u0010\u0019\u001a\u00020\u001a2\u0006\u0010\u001b\u001a\u00020\u001c2\u0006\u0010\u001d\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010!\u001a\u00020\"H\u0002J\u0010\u0010#\u001a\u00020$2\u0006\u0010%\u001a\u00020&H\u0002J\u0010\u0010'\u001a\u00020(2\u0006\u0010)\u001a\u00020\u001eH\u0002J\u0010\u0010*\u001a\u00020(2\u0006\u0010)\u001a\u00020\u001eH\u0002JC\u0010+\u001a\u00020,2\u0006\u0010-\u001a\u00020.2\u0006\u0010\u001b\u001a\u00020\u001c2\u0006\u0010\u0019\u001a\u00020\u001a2\u0006\u0010/\u001a\u0002002\b\u00101\u001a\u0004\u0018\u0001022\u0006\u0010!\u001a\u00020\"H\u0096Bø\u0001\u0000¢\u0006\u0002\u00103J\u0010\u00104\u001a\u00020\u001e2\u0006\u00105\u001a\u00020$H\u0002R\u000e\u0010\u0010\u001a\u00020\u0011X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0012\u001a\u00020\u0013X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\f\u001a\u00020\rX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0014\u001a\u00020\u0015X\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u00066"}, d2 = {"Lcom/unity3d/ads/core/domain/AndroidLoad;", "Lcom/unity3d/ads/core/domain/Load;", "defaultDispatcher", "Lkotlinx/coroutines/CoroutineDispatcher;", "getAdRequest", "Lcom/unity3d/ads/core/domain/GetAdRequest;", "getAdPlayerConfigRequest", "Lcom/unity3d/ads/core/domain/GetAdPlayerConfigRequest;", "getRequestPolicy", "Lcom/unity3d/ads/core/domain/GetRequestPolicy;", "handleGatewayAdResponse", "Lcom/unity3d/ads/core/domain/HandleGatewayAdResponse;", "sessionRepository", "Lcom/unity3d/ads/core/data/repository/SessionRepository;", "gatewayClient", "Lcom/unity3d/ads/gatewayclient/GatewayClient;", "adRepository", "Lcom/unity3d/ads/core/data/repository/AdRepository;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "validateExtrasSize", "Lcom/unity3d/ads/core/domain/ValidateExtrasSize;", "(Lkotlinx/coroutines/CoroutineDispatcher;Lcom/unity3d/ads/core/domain/GetAdRequest;Lcom/unity3d/ads/core/domain/GetAdPlayerConfigRequest;Lcom/unity3d/ads/core/domain/GetRequestPolicy;Lcom/unity3d/ads/core/domain/HandleGatewayAdResponse;Lcom/unity3d/ads/core/data/repository/SessionRepository;Lcom/unity3d/ads/gatewayclient/GatewayClient;Lcom/unity3d/ads/core/data/repository/AdRepository;Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;Lcom/unity3d/ads/core/domain/ValidateExtrasSize;)V", "getTmpAdObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "opportunityId", "Lcom/google/protobuf/ByteString;", "placement", "", HandleInvocationsFromAdViewer.KEY_IS_HEADER_BIDDING, "", "adType", "Lgatewayprotocol/v1/DiagnosticEventRequestOuterClass$DiagnosticAdType;", HandleInvocationsFromAdViewer.KEY_LOAD_OPTIONS, "Lcom/unity3d/ads/UnityAdsLoadOptions;", "handleGatewayException", "Lcom/unity3d/ads/core/data/model/LoadResult$Failure;", "e", "Lcom/unity3d/ads/core/data/model/exception/UnityAdsNetworkException;", "incrementLoadRequestAdmCount", "", "isBanner", "incrementLoadRequestCount", "invoke", "Lcom/unity3d/ads/core/data/model/LoadResult;", "context", "Landroid/content/Context;", "headerBiddingAdMarkup", "Lgatewayprotocol/v1/HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup;", "bannerSize", "Lgatewayprotocol/v1/AdRequestOuterClass$BannerSize;", "(Landroid/content/Context;Ljava/lang/String;Lcom/google/protobuf/ByteString;Lgatewayprotocol/v1/HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup;Lgatewayprotocol/v1/AdRequestOuterClass$BannerSize;Lcom/unity3d/ads/UnityAdsLoadOptions;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "isCachePhaseFailure", "failure", "unity-ads_defaultRelease"})
public final class AndroidLoad implements Load {

    @NotNull
    private final CoroutineDispatcher defaultDispatcher;

    @NotNull
    private final GetAdRequest getAdRequest;

    @NotNull
    private final GetAdPlayerConfigRequest getAdPlayerConfigRequest;

    @NotNull
    private final GetRequestPolicy getRequestPolicy;

    @NotNull
    private final HandleGatewayAdResponse handleGatewayAdResponse;

    @NotNull
    private final SessionRepository sessionRepository;

    @NotNull
    private final GatewayClient gatewayClient;

    @NotNull
    private final AdRepository adRepository;

    @NotNull
    private final SendDiagnosticEvent sendDiagnosticEvent;

    @NotNull
    private final ValidateExtrasSize validateExtrasSize;

    public AndroidLoad(@NotNull CoroutineDispatcher defaultDispatcher, @NotNull GetAdRequest getAdRequest, @NotNull GetAdPlayerConfigRequest getAdPlayerConfigRequest, @NotNull GetRequestPolicy getRequestPolicy, @NotNull HandleGatewayAdResponse handleGatewayAdResponse, @NotNull SessionRepository sessionRepository, @NotNull GatewayClient gatewayClient, @NotNull AdRepository adRepository, @NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull ValidateExtrasSize validateExtrasSize) {
        Intrinsics.checkNotNullParameter(defaultDispatcher, "defaultDispatcher");
        Intrinsics.checkNotNullParameter(getAdRequest, "getAdRequest");
        Intrinsics.checkNotNullParameter(getAdPlayerConfigRequest, "getAdPlayerConfigRequest");
        Intrinsics.checkNotNullParameter(getRequestPolicy, "getRequestPolicy");
        Intrinsics.checkNotNullParameter(handleGatewayAdResponse, "handleGatewayAdResponse");
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        Intrinsics.checkNotNullParameter(gatewayClient, "gatewayClient");
        Intrinsics.checkNotNullParameter(adRepository, "adRepository");
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(validateExtrasSize, "validateExtrasSize");
        this.defaultDispatcher = defaultDispatcher;
        this.getAdRequest = getAdRequest;
        this.getAdPlayerConfigRequest = getAdPlayerConfigRequest;
        this.getRequestPolicy = getRequestPolicy;
        this.handleGatewayAdResponse = handleGatewayAdResponse;
        this.sessionRepository = sessionRepository;
        this.gatewayClient = gatewayClient;
        this.adRepository = adRepository;
        this.sendDiagnosticEvent = sendDiagnosticEvent;
        this.validateExtrasSize = validateExtrasSize;
    }

    public static final /* synthetic */ SessionRepository access$getSessionRepository$p(AndroidLoad $this) {
        return $this.sessionRepository;
    }

    public static final /* synthetic */ boolean access$isCachePhaseFailure(AndroidLoad $this, Failure failure) {
        return $this.isCachePhaseFailure(failure);
    }

    public static final /* synthetic */ ValidateExtrasSize access$getValidateExtrasSize$p(AndroidLoad $this) {
        return $this.validateExtrasSize;
    }

    public static final /* synthetic */ GatewayClient access$getGatewayClient$p(AndroidLoad $this) {
        return $this.gatewayClient;
    }

    public static final /* synthetic */ SendDiagnosticEvent access$getSendDiagnosticEvent$p(AndroidLoad $this) {
        return $this.sendDiagnosticEvent;
    }

    public static final /* synthetic */ AdObject access$getTmpAdObject(AndroidLoad $this, ByteString opportunityId, String placement, boolean isHeaderBidding, DiagnosticEventRequestOuterClass$DiagnosticAdType adType, UnityAdsLoadOptions loadOptions) {
        return $this.getTmpAdObject(opportunityId, placement, isHeaderBidding, adType, loadOptions);
    }

    public static final /* synthetic */ void access$incrementLoadRequestCount(AndroidLoad $this, boolean isBanner) {
        $this.incrementLoadRequestCount(isBanner);
    }

    public static final /* synthetic */ GetAdRequest access$getGetAdRequest$p(AndroidLoad $this) {
        return $this.getAdRequest;
    }

    public static final /* synthetic */ GetRequestPolicy access$getGetRequestPolicy$p(AndroidLoad $this) {
        return $this.getRequestPolicy;
    }

    public static final /* synthetic */ void access$incrementLoadRequestAdmCount(AndroidLoad $this, boolean isBanner) {
        $this.incrementLoadRequestAdmCount(isBanner);
    }

    public static final /* synthetic */ GetAdPlayerConfigRequest access$getGetAdPlayerConfigRequest$p(AndroidLoad $this) {
        return $this.getAdPlayerConfigRequest;
    }

    public static final /* synthetic */ HandleGatewayAdResponse access$getHandleGatewayAdResponse$p(AndroidLoad $this) {
        return $this.handleGatewayAdResponse;
    }

    public static final /* synthetic */ AdRepository access$getAdRepository$p(AndroidLoad $this) {
        return $this.adRepository;
    }

    public static final /* synthetic */ Failure access$handleGatewayException(AndroidLoad $this, UnityAdsNetworkException e) {
        return $this.handleGatewayException(e);
    }

    @Override // com.unity3d.ads.core.domain.Load
    @Nullable
    public Object invoke(@NotNull Context context, @NotNull String placement, @NotNull ByteString opportunityId, @NotNull HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup headerBiddingAdMarkup, @Nullable AdRequestOuterClass$BannerSize bannerSize, @NotNull UnityAdsLoadOptions loadOptions, @NotNull Continuation<? super LoadResult> continuation) {
        return BuildersKt.withContext(this.defaultDispatcher, new AndroidLoad$invoke$2(bannerSize, this, headerBiddingAdMarkup, opportunityId, placement, loadOptions, context, null), continuation);
    }

    /* JADX WARN: Code duplicated, block: B:21:0x0057  */
    private final Failure handleGatewayException(UnityAdsNetworkException e) {
        ErrorOuterClass$PublicErrorCode errorCode;
        String loadErrorMsg;
        if (e instanceof NetworkTimeoutException) {
            errorCode = ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_TIMEOUT;
        } else if (e instanceof GatewayException) {
            errorCode = ((GatewayException) e).getErrorCode();
            if (errorCode == null) {
                errorCode = ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NETWORK;
            }
        } else {
            errorCode = ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NETWORK;
        }
        ErrorOuterClass$PublicErrorCode errorOuterClass$PublicErrorCode = errorCode;
        if (e instanceof NetworkTimeoutException) {
            loadErrorMsg = UnityAdsErrorKt.MSG_BOLD_LOAD_FAIL_TIME_OUT;
        } else if (e instanceof GatewayException) {
            ErrorOuterClass$PublicErrorCode errorCode2 = ((GatewayException) e).getErrorCode();
            if (errorCode2 != null) {
                loadErrorMsg = UnityAdsErrorKt.getLoadErrorMsg(errorCode2);
                if (loadErrorMsg == null) {
                    loadErrorMsg = UnityAdsErrorKt.getLoadErrorMsg(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NETWORK);
                }
            } else {
                loadErrorMsg = UnityAdsErrorKt.getLoadErrorMsg(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NETWORK);
            }
        } else {
            loadErrorMsg = UnityAdsErrorKt.getLoadErrorMsg(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NETWORK);
        }
        return new Failure(errorOuterClass$PublicErrorCode, loadErrorMsg, e, e instanceof NetworkTimeoutException ? "timeout" : "gateway", e.getMessage(), false, 32, null);
    }

    /* JADX WARN: Can't fix incorrect switch cases order, some code will duplicate */
    /* JADX WARN: Code duplicated, block: B:12:0x004d A[RETURN, SYNTHETIC] */
    /* JADX WARN: Code duplicated, block: B:13:0x0051 A[ORIG_RETURN, RETURN] */
    private final boolean isCachePhaseFailure(Failure failure) {
        switch (failure.getReason()) {
            case "no_webview_entry_point":
            case "invalid_url":
            case "adviewer":
                return true;
            default:
                return false;
        }
    }

    private final void incrementLoadRequestCount(boolean isBanner) {
        if (isBanner) {
            this.sessionRepository.incrementBannerLoadRequestCount();
        } else {
            this.sessionRepository.incrementLoadRequestCount();
        }
    }

    private final void incrementLoadRequestAdmCount(boolean isBanner) {
        if (isBanner) {
            this.sessionRepository.incrementBannerLoadRequestAdmCount();
        } else {
            this.sessionRepository.incrementLoadRequestAdmCount();
        }
    }

    private final AdObject getTmpAdObject(ByteString opportunityId, String placement, boolean isHeaderBidding, DiagnosticEventRequestOuterClass$DiagnosticAdType adType, UnityAdsLoadOptions loadOptions) {
        return SendDiagnosticEvent$Companion.getTmpAdObjectForEventSending$default(SendDiagnosticEvent.Companion, opportunityId, placement, isHeaderBidding, loadOptions, adType, false, 32, null);
    }
}