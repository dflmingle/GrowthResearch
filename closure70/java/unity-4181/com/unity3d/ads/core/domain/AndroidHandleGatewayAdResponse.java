package com.unity3d.ads.core.domain;

import android.content.Context;
import android.util.Base64;
import com.google.protobuf.ByteString;
import com.unity3d.ads.UnityAdsErrorKt;
import com.unity3d.ads.UnityAdsLoadOptions;
import com.unity3d.ads.adplayer.AdPlayer;
import com.unity3d.ads.adplayer.AdPlayerScope;
import com.unity3d.ads.adplayer.AndroidWebViewContainer;
import com.unity3d.ads.adplayer.WebViewBridge;
import com.unity3d.ads.adplayer.WebViewContainer;
import com.unity3d.ads.adplayer.model.Error;
import com.unity3d.ads.adplayer.model.LoadEvent;
import com.unity3d.ads.adplayer.model.LoadEvent$Completed;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.model.CoroutineOpportunity;
import com.unity3d.ads.core.data.model.Failure;
import com.unity3d.ads.core.data.model.LoadResult;
import com.unity3d.ads.core.data.model.Success;
import com.unity3d.ads.core.data.model.WebViewConfiguration;
import com.unity3d.ads.core.data.repository.AdRepository;
import com.unity3d.ads.core.data.repository.CampaignRepository;
import com.unity3d.ads.core.data.repository.DeviceInfoRepository;
import com.unity3d.ads.core.data.repository.SessionRepository;
import com.unity3d.ads.core.domain.adload.WebViewLessLoadStrategy;
import com.unity3d.ads.core.domain.events.GetOperativeEventApi;
import com.unity3d.ads.core.extensions.ProtobufExtensionsKt;
import com.unity3d.ads.core.extensions.TimeExtensionsKt;
import com.unity3d.services.UnityAdsConstants$Messages;
import com.unity3d.services.core.properties.SdkProperties;
import gatewayprotocol.v1.AdResponseOuterClass$AdResponse;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticAdType;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.ErrorOuterClass$Error;
import gatewayprotocol.v1.ErrorOuterClass$PublicErrorCode;
import gatewayprotocol.v1.OperativeEventErrorDataKt$Dsl;
import gatewayprotocol.v1.OperativeEventErrorDataKt$Dsl$Companion;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorData;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorData$Builder;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorType;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventType;
import java.net.URI;
import java.util.Map;
import java.util.concurrent.CancellationException;
import kotlin.Metadata;
import kotlin.Result;
import kotlin.Result$Companion;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.Ref$ObjectRef;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import kotlin.time.Duration;
import kotlin.time.DurationUnit;
import kotlin.time.TimeSource$Monotonic;
import kotlin.time.TimeSource$Monotonic$ValueTimeMark;
import kotlin.time.TimedValue;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.CoroutineScopeKt;
import kotlinx.coroutines.CoroutineStart;
import kotlinx.coroutines.NonCancellable;
import kotlinx.coroutines.flow.FlowKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.json.JSONObject;

/* JADX INFO: compiled from: AndroidHandleGatewayAdResponse.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000¶\u0001\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u0003\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000b\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0000\u0018\u00002\u00020\u0001Bu\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\t\u0012\u0006\u0010\n\u001a\u00020\u000b\u0012\u0006\u0010\f\u001a\u00020\r\u0012\u0006\u0010\u000e\u001a\u00020\u000f\u0012\u0006\u0010\u0010\u001a\u00020\u0011\u0012\u0006\u0010\u0012\u001a\u00020\u0013\u0012\u0006\u0010\u0014\u001a\u00020\u0015\u0012\u0006\u0010\u0016\u001a\u00020\u0017\u0012\u0006\u0010\u0018\u001a\u00020\u0019\u0012\u0006\u0010\u001a\u001a\u00020\u001b\u0012\u0006\u0010\u001c\u001a\u00020\u001d¢\u0006\u0002\u0010\u001eJ3\u0010\u001f\u001a\u00020 2\u0006\u0010!\u001a\u00020\"2\u0006\u0010#\u001a\u00020$2\u0006\u0010%\u001a\u00020&2\b\u0010'\u001a\u0004\u0018\u00010(H\u0082@ø\u0001\u0000¢\u0006\u0002\u0010)JQ\u0010*\u001a\u00020+2\u0006\u0010,\u001a\u00020-2\u0006\u0010#\u001a\u00020$2\u0006\u0010%\u001a\u00020&2\u0006\u0010.\u001a\u00020/2\u0006\u00100\u001a\u0002012\u0006\u00102\u001a\u0002032\u0006\u00104\u001a\u0002052\u0006\u00106\u001a\u000205H\u0096Bø\u0001\u0000¢\u0006\u0002\u00107J)\u00108\u001a\u00020 2\u0006\u00109\u001a\u00020:2\u0006\u0010;\u001a\u0002012\u0006\u0010<\u001a\u00020=H\u0082@ø\u0001\u0000¢\u0006\u0002\u0010>R\u000e\u0010\u0014\u001a\u00020\u0015X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0018\u001a\u00020\u0019X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\f\u001a\u00020\rX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0016\u001a\u00020\u0017X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0012\u001a\u00020\u0013X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0010\u001a\u00020\u0011X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u001c\u001a\u00020\u001dX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u001a\u001a\u00020\u001bX\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006?"}, d2 = {"Lcom/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse;", "Lcom/unity3d/ads/core/domain/HandleGatewayAdResponse;", "adRepository", "Lcom/unity3d/ads/core/data/repository/AdRepository;", "getWebViewContainerUseCase", "Lcom/unity3d/ads/core/domain/AndroidGetWebViewContainerUseCase;", "getWebViewBridge", "Lcom/unity3d/ads/core/domain/GetWebViewBridgeUseCase;", "deviceInfoRepository", "Lcom/unity3d/ads/core/data/repository/DeviceInfoRepository;", "getHandleInvocationsFromAdViewer", "Lcom/unity3d/ads/core/domain/HandleInvocationsFromAdViewer;", "campaignRepository", "Lcom/unity3d/ads/core/data/repository/CampaignRepository;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "getOperativeEventApi", "Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;", "getLatestWebViewConfiguration", "Lcom/unity3d/ads/core/domain/GetLatestWebViewConfiguration;", "adPlayerScope", "Lcom/unity3d/ads/adplayer/AdPlayerScope;", "getAdPlayer", "Lcom/unity3d/ads/core/domain/GetAdPlayer;", "cacheWebViewAssets", "Lcom/unity3d/ads/core/domain/CacheWebViewAssets;", "webViewLessLoadStrategy", "Lcom/unity3d/ads/core/domain/adload/WebViewLessLoadStrategy;", "sessionRepository", "Lcom/unity3d/ads/core/data/repository/SessionRepository;", "(Lcom/unity3d/ads/core/data/repository/AdRepository;Lcom/unity3d/ads/core/domain/AndroidGetWebViewContainerUseCase;Lcom/unity3d/ads/core/domain/GetWebViewBridgeUseCase;Lcom/unity3d/ads/core/data/repository/DeviceInfoRepository;Lcom/unity3d/ads/core/domain/HandleInvocationsFromAdViewer;Lcom/unity3d/ads/core/data/repository/CampaignRepository;Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;Lcom/unity3d/ads/core/domain/GetLatestWebViewConfiguration;Lcom/unity3d/ads/adplayer/AdPlayerScope;Lcom/unity3d/ads/core/domain/GetAdPlayer;Lcom/unity3d/ads/core/domain/CacheWebViewAssets;Lcom/unity3d/ads/core/domain/adload/WebViewLessLoadStrategy;Lcom/unity3d/ads/core/data/repository/SessionRepository;)V", "cleanup", "", "t", "", "opportunityId", "Lcom/google/protobuf/ByteString;", "response", "Lgatewayprotocol/v1/AdResponseOuterClass$AdResponse;", "adPlayer", "Lcom/unity3d/ads/adplayer/AdPlayer;", "(Ljava/lang/Throwable;Lcom/google/protobuf/ByteString;Lgatewayprotocol/v1/AdResponseOuterClass$AdResponse;Lcom/unity3d/ads/adplayer/AdPlayer;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "invoke", "Lcom/unity3d/ads/core/data/model/LoadResult;", HandleInvocationsFromAdViewer.KEY_LOAD_OPTIONS, "Lcom/unity3d/ads/UnityAdsLoadOptions;", "context", "Landroid/content/Context;", HandleInvocationsFromAdViewer.KEY_PLACEMENT_ID, "", "adType", "Lgatewayprotocol/v1/DiagnosticEventRequestOuterClass$DiagnosticAdType;", HandleInvocationsFromAdViewer.KEY_IS_HEADER_BIDDING, "", "forceWebViewLoad", "(Lcom/unity3d/ads/UnityAdsLoadOptions;Lcom/google/protobuf/ByteString;Lgatewayprotocol/v1/AdResponseOuterClass$AdResponse;Landroid/content/Context;Ljava/lang/String;Lgatewayprotocol/v1/DiagnosticEventRequestOuterClass$DiagnosticAdType;ZZLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "loadUrl", "adObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "webViewUrl", "webviewContainer", "Lcom/unity3d/ads/adplayer/WebViewContainer;", "(Lcom/unity3d/ads/core/data/model/AdObject;Ljava/lang/String;Lcom/unity3d/ads/adplayer/WebViewContainer;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "unity-ads_defaultRelease"})
@SourceDebugExtension({"SMAP\nAndroidHandleGatewayAdResponse.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AndroidHandleGatewayAdResponse.kt\ncom/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n+ 3 measureTime.kt\nkotlin/time/MeasureTimeKt\n+ 4 OperativeEventErrorDataKt.kt\ngatewayprotocol/v1/OperativeEventErrorDataKtKt\n*L\n1#1,287:1\n1#2:288\n1#2:314\n79#3,5:289\n113#3,7:294\n79#3,5:301\n113#3,7:306\n10#4:313\n*S KotlinDebug\n*F\n+ 1 AndroidHandleGatewayAdResponse.kt\ncom/unity3d/ads/core/domain/AndroidHandleGatewayAdResponse\n*L\n274#1:314\n175#1:289,5\n175#1:294,7\n254#1:301,5\n254#1:306,7\n274#1:313\n*E\n"})
public final class AndroidHandleGatewayAdResponse implements HandleGatewayAdResponse {

    @NotNull
    private final AdRepository adRepository;

    @NotNull
    private final AndroidGetWebViewContainerUseCase getWebViewContainerUseCase;

    @NotNull
    private final GetWebViewBridgeUseCase getWebViewBridge;

    @NotNull
    private final DeviceInfoRepository deviceInfoRepository;

    @NotNull
    private final HandleInvocationsFromAdViewer getHandleInvocationsFromAdViewer;

    @NotNull
    private final CampaignRepository campaignRepository;

    @NotNull
    private final SendDiagnosticEvent sendDiagnosticEvent;

    @NotNull
    private final GetOperativeEventApi getOperativeEventApi;

    @NotNull
    private final GetLatestWebViewConfiguration getLatestWebViewConfiguration;

    @NotNull
    private final AdPlayerScope adPlayerScope;

    @NotNull
    private final GetAdPlayer getAdPlayer;

    @NotNull
    private final CacheWebViewAssets cacheWebViewAssets;

    @NotNull
    private final WebViewLessLoadStrategy webViewLessLoadStrategy;

    @NotNull
    private final SessionRepository sessionRepository;

    public AndroidHandleGatewayAdResponse(@NotNull AdRepository adRepository, @NotNull AndroidGetWebViewContainerUseCase getWebViewContainerUseCase, @NotNull GetWebViewBridgeUseCase getWebViewBridge, @NotNull DeviceInfoRepository deviceInfoRepository, @NotNull HandleInvocationsFromAdViewer getHandleInvocationsFromAdViewer, @NotNull CampaignRepository campaignRepository, @NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull GetOperativeEventApi getOperativeEventApi, @NotNull GetLatestWebViewConfiguration getLatestWebViewConfiguration, @NotNull AdPlayerScope adPlayerScope, @NotNull GetAdPlayer getAdPlayer, @NotNull CacheWebViewAssets cacheWebViewAssets, @NotNull WebViewLessLoadStrategy webViewLessLoadStrategy, @NotNull SessionRepository sessionRepository) {
        Intrinsics.checkNotNullParameter(adRepository, "adRepository");
        Intrinsics.checkNotNullParameter(getWebViewContainerUseCase, "getWebViewContainerUseCase");
        Intrinsics.checkNotNullParameter(getWebViewBridge, "getWebViewBridge");
        Intrinsics.checkNotNullParameter(deviceInfoRepository, "deviceInfoRepository");
        Intrinsics.checkNotNullParameter(getHandleInvocationsFromAdViewer, "getHandleInvocationsFromAdViewer");
        Intrinsics.checkNotNullParameter(campaignRepository, "campaignRepository");
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(getOperativeEventApi, "getOperativeEventApi");
        Intrinsics.checkNotNullParameter(getLatestWebViewConfiguration, "getLatestWebViewConfiguration");
        Intrinsics.checkNotNullParameter(adPlayerScope, "adPlayerScope");
        Intrinsics.checkNotNullParameter(getAdPlayer, "getAdPlayer");
        Intrinsics.checkNotNullParameter(cacheWebViewAssets, "cacheWebViewAssets");
        Intrinsics.checkNotNullParameter(webViewLessLoadStrategy, "webViewLessLoadStrategy");
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        this.adRepository = adRepository;
        this.getWebViewContainerUseCase = getWebViewContainerUseCase;
        this.getWebViewBridge = getWebViewBridge;
        this.deviceInfoRepository = deviceInfoRepository;
        this.getHandleInvocationsFromAdViewer = getHandleInvocationsFromAdViewer;
        this.campaignRepository = campaignRepository;
        this.sendDiagnosticEvent = sendDiagnosticEvent;
        this.getOperativeEventApi = getOperativeEventApi;
        this.getLatestWebViewConfiguration = getLatestWebViewConfiguration;
        this.adPlayerScope = adPlayerScope;
        this.getAdPlayer = getAdPlayer;
        this.cacheWebViewAssets = cacheWebViewAssets;
        this.webViewLessLoadStrategy = webViewLessLoadStrategy;
        this.sessionRepository = sessionRepository;
    }

    public static final /* synthetic */ Object access$loadUrl(AndroidHandleGatewayAdResponse $this, AdObject adObject, String webViewUrl, WebViewContainer webviewContainer, Continuation $completion) {
        return $this.loadUrl(adObject, webViewUrl, webviewContainer, $completion);
    }

    public static final /* synthetic */ Object access$cleanup(AndroidHandleGatewayAdResponse $this, Throwable t, ByteString opportunityId, AdResponseOuterClass$AdResponse response, AdPlayer adPlayer, Continuation $completion) {
        return $this.cleanup(t, opportunityId, response, adPlayer, $completion);
    }

    /* JADX WARN: Code duplicated, block: B:107:0x063c A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:108:0x0642 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:111:0x0773 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:117:0x0810  */
    /* JADX WARN: Code duplicated, block: B:124:0x08b8  */
    /* JADX WARN: Code duplicated, block: B:131:0x0919 A[Catch: CancellationException -> 0x0a8a, TRY_LEAVE, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:134:0x099f  */
    /* JADX WARN: Code duplicated, block: B:140:0x0a05 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:142:0x0a46 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:144:0x0a4e  */
    /* JADX WARN: Code duplicated, block: B:147:0x0a56 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:149:0x0a5e A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:153:0x0a6f A[ADDED_TO_REGION, REMOVE] */
    /* JADX WARN: Code duplicated, block: B:155:0x0a74 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:166:0x0b12  */
    /* JADX WARN: Code duplicated, block: B:175:? A[RETURN, SYNTHETIC] */
    /* JADX WARN: Code duplicated, block: B:20:0x00b6 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:36:0x01d9 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:38:0x01e8 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:40:0x01ff A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:42:0x0226  */
    /* JADX WARN: Code duplicated, block: B:43:0x022a  */
    /* JADX WARN: Code duplicated, block: B:48:0x02a5  */
    /* JADX WARN: Code duplicated, block: B:54:0x032f  */
    /* JADX WARN: Code duplicated, block: B:55:0x0333  */
    /* JADX WARN: Code duplicated, block: B:57:0x0337 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:59:0x034e A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:61:0x0370  */
    /* JADX WARN: Code duplicated, block: B:62:0x0375  */
    /* JADX WARN: Code duplicated, block: B:65:0x037b A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:73:0x03d3  */
    /* JADX WARN: Code duplicated, block: B:76:0x0402 A[Catch: CancellationException -> 0x0a8a, TryCatch #2 {CancellationException -> 0x0a8a, blocks: (B:11:0x0086, B:13:0x008e, B:15:0x00a7, B:17:0x00ae, B:21:0x00bd, B:20:0x00b6, B:23:0x00cf, B:25:0x00d9, B:27:0x00ee, B:34:0x01b8, B:36:0x01d9, B:38:0x01e8, B:45:0x023a, B:52:0x031e, B:57:0x0337, B:59:0x034e, B:65:0x037b, B:67:0x0382, B:71:0x03ab, B:74:0x03d6, B:76:0x0402, B:78:0x040a, B:80:0x0411, B:82:0x041b, B:86:0x0434, B:94:0x04b5, B:95:0x04dc, B:102:0x05e0, B:105:0x05fb, B:107:0x063c, B:109:0x0645, B:111:0x0773, B:113:0x0785, B:129:0x090f, B:131:0x0919, B:138:0x09e3, B:140:0x0a05, B:142:0x0a46, B:147:0x0a56, B:149:0x0a5e, B:155:0x0a74, B:156:0x0a80, B:114:0x07af, B:121:0x0864, B:128:0x090c, B:108:0x0642, B:104:0x05ed, B:69:0x0393, B:40:0x01ff, B:44:0x022b, B:33:0x01b0, B:51:0x0316, B:92:0x04ac, B:101:0x05d8, B:120:0x085c, B:127:0x0904, B:137:0x09db), top: B:170:0x0046, inners: #0, #1 }] */
    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    /* JADX WARN: Code duplicated, block: B:98:0x055b  */
    @Override // com.unity3d.ads.core.domain.HandleGatewayAdResponse
    @Nullable
    public Object invoke(@NotNull UnityAdsLoadOptions loadOptions, @NotNull ByteString opportunityId, @NotNull AdResponseOuterClass$AdResponse response, @NotNull Context context, @NotNull String placementId, @NotNull DiagnosticEventRequestOuterClass$DiagnosticAdType adType, boolean isHeaderBidding, boolean forceWebViewLoad, @NotNull Continuation<? super LoadResult> continuation) throws Throwable {
        AndroidHandleGatewayAdResponse$invoke$1 androidHandleGatewayAdResponse$invoke$1;
        Ref$ObjectRef adPlayer;
        Object obj;
        Throwable cause;
        long loadAdViewerStartedTime;
        AdObject adObject;
        Object objSingle;
        LoadEvent$Completed loadEvent$Completed;
        LoadEvent loadEvent;
        String objectId;
        boolean z;
        boolean z2;
        Object result;
        DiagnosticEventRequestOuterClass$DiagnosticEventType diagnosticEventRequestOuterClass$DiagnosticEventType;
        AndroidWebViewContainer webviewContainer;
        long mark$iv$iv;
        String base64ImpressionConfiguration;
        String webViewUrl;
        AdObject tmpAdObject;
        Object objInvoke;
        CoroutineScope adScope;
        WebViewConfiguration webviewConfiguration;
        Object objInvoke2;
        boolean z3;
        String it;
        String entryPoint;
        String selectedUrl;
        String query;
        AdObject adObject2;
        boolean z4;
        String errorText;
        if (continuation instanceof AndroidHandleGatewayAdResponse$invoke$1) {
            androidHandleGatewayAdResponse$invoke$1 = (AndroidHandleGatewayAdResponse$invoke$1) continuation;
            if ((androidHandleGatewayAdResponse$invoke$1.label & Integer.MIN_VALUE) != 0) {
                androidHandleGatewayAdResponse$invoke$1.label -= Integer.MIN_VALUE;
            } else {
                androidHandleGatewayAdResponse$invoke$1 = new AndroidHandleGatewayAdResponse$invoke$1(this, continuation);
            }
        } else {
            androidHandleGatewayAdResponse$invoke$1 = new AndroidHandleGatewayAdResponse$invoke$1(this, continuation);
        }
        Object $result = androidHandleGatewayAdResponse$invoke$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        try {
            try {
                switch (androidHandleGatewayAdResponse$invoke$1.label) {
                    case 0:
                        ResultKt.throwOnFailure($result);
                        adPlayer = new Ref$ObjectRef();
                        if (response.hasError()) {
                            ErrorOuterClass$PublicErrorCode errorCode = response.getError().getErrorCode();
                            Intrinsics.checkNotNullExpressionValue(errorCode, "response.error.errorCode");
                            ErrorOuterClass$Error error = response.getError();
                            if (error != null) {
                                ErrorOuterClass$PublicErrorCode errorCode2 = error.getErrorCode();
                                if (errorCode2 != null) {
                                    errorText = UnityAdsErrorKt.getLoadErrorMsg(errorCode2);
                                    if (errorText == null) {
                                        errorText = response.getError().getErrorText();
                                    }
                                } else {
                                    errorText = response.getError().getErrorText();
                                }
                            } else {
                                errorText = response.getError().getErrorText();
                            }
                            return new Failure(errorCode, errorText, null, "gateway", response.getError().getErrorText(), false, 36, null);
                        }
                        if (response.getAdData().isEmpty()) {
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_LOAD_NO_FILL, UnityAdsErrorKt.MSG_BOLD_LOAD_FAIL_NO_FILL, null, "no_fill", null, false, 52, null);
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.Z$0 = isHeaderBidding;
                        androidHandleGatewayAdResponse$invoke$1.Z$1 = forceWebViewLoad;
                        androidHandleGatewayAdResponse$invoke$1.label = 1;
                        objInvoke2 = this.getLatestWebViewConfiguration.invoke(response.getWebviewConfiguration().getEntryPoint(), Boxing.boxInt(response.getWebviewConfiguration().getVersion()), response.getWebviewConfiguration().getAdditionalFilesList(), response.getWebviewConfiguration().getType(), androidHandleGatewayAdResponse$invoke$1);
                        if (objInvoke2 == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        webviewConfiguration = (WebViewConfiguration) objInvoke2;
                        adScope = CoroutineScopeKt.plus(this.adPlayerScope, new CoroutineOpportunity(opportunityId));
                        if (forceWebViewLoad) {
                            adObject2 = this.adRepository.getAd(opportunityId);
                            if (adObject2 == null) {
                                return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "webviewless_ad_not_found", null, false, 52, null);
                            }
                        } else {
                            ByteString trackingToken = response.getTrackingToken();
                            ByteString byteString = opportunityId;
                            String str = placementId;
                            Intrinsics.checkNotNullExpressionValue(trackingToken, HandleInvocationsFromAdViewer.KEY_TRACKING_TOKEN);
                            UnityAdsLoadOptions unityAdsLoadOptions = loadOptions;
                            if (isHeaderBidding) {
                                z4 = true;
                            } else {
                                z4 = false;
                            }
                            adObject2 = new AdObject(adScope, byteString, str, trackingToken, false, null, null, null, false, null, null, null, unityAdsLoadOptions, z4, adType, null, null, null, null, null, null, 2068464, null);
                        }
                        tmpAdObject = adObject2;
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = webviewConfiguration;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = adScope;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = tmpAdObject;
                        androidHandleGatewayAdResponse$invoke$1.Z$0 = isHeaderBidding;
                        androidHandleGatewayAdResponse$invoke$1.Z$1 = forceWebViewLoad;
                        androidHandleGatewayAdResponse$invoke$1.label = 2;
                        if (this.cacheWebViewAssets.invoke(webviewConfiguration, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        if (webviewConfiguration.getEntryPoint().length() == 0) {
                            z3 = true;
                        } else {
                            z3 = false;
                        }
                        if (z3) {
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "no_webview_entry_point", null, false, 52, null);
                        }
                        it = SdkProperties.getConfigUrl();
                        Intrinsics.checkNotNullExpressionValue(it, "it");
                        if (StringsKt.endsWith$default(it, ".html", false, 2, (Object) null)) {
                            entryPoint = it;
                        } else {
                            entryPoint = null;
                        }
                        if (entryPoint == null) {
                            entryPoint = webviewConfiguration.getEntryPoint();
                        }
                        selectedUrl = entryPoint;
                        try {
                            URI url = new URI(selectedUrl);
                            StringBuilder sbAppend = new StringBuilder().append("?platform=android&mode=ad-viewer&webviewType=").append(webviewConfiguration.getType()).append('&');
                            query = url.getQuery();
                            if (query == null) {
                                query = "";
                            }
                            String query2 = sbAppend.append(query).toString();
                            webViewUrl = StringsKt.substringBeforeLast$default(selectedUrl, "?", (String) null, 2, (Object) null) + query2;
                            if (forceWebViewLoad && adType != DiagnosticEventRequestOuterClass$DiagnosticAdType.DIAGNOSTIC_AD_TYPE_BANNER && response.hasCampaignMetadata() && response.getCampaignMetadata().getAssetsToCacheCount() > 0) {
                                WebViewLessLoadStrategy webViewLessLoadStrategy = this.webViewLessLoadStrategy;
                                CoroutineScope coroutineScope = adScope;
                                UnityAdsLoadOptions unityAdsLoadOptions2 = loadOptions;
                                ByteString byteString2 = opportunityId;
                                AdResponseOuterClass$AdResponse adResponseOuterClass$AdResponse = response;
                                String str2 = placementId;
                                DiagnosticEventRequestOuterClass$DiagnosticAdType diagnosticEventRequestOuterClass$DiagnosticAdType = adType;
                                boolean z5 = isHeaderBidding;
                                androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                                androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                                androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                                androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                                androidHandleGatewayAdResponse$invoke$1.L$4 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$5 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                                androidHandleGatewayAdResponse$invoke$1.label = 3;
                                Object objInvoke3 = webViewLessLoadStrategy.invoke(coroutineScope, webViewUrl, unityAdsLoadOptions2, byteString2, adResponseOuterClass$AdResponse, str2, diagnosticEventRequestOuterClass$DiagnosticAdType, z5, androidHandleGatewayAdResponse$invoke$1);
                                return objInvoke3 == coroutine_suspended ? coroutine_suspended : objInvoke3;
                            }
                            base64ImpressionConfiguration = Base64.encodeToString(response.getImpressionConfiguration().toByteArray(), 2);
                            TimeSource$Monotonic $this$measureTimedValue$iv$iv = TimeSource$Monotonic.INSTANCE;
                            mark$iv$iv = $this$measureTimedValue$iv$iv.markNow-z9LOYto();
                            AndroidHandleGatewayAdResponse androidHandleGatewayAdResponse = this;
                            Result$Companion result$Companion = Result.Companion;
                            AndroidHandleGatewayAdResponse $this$invoke_u24lambda_u242_u24lambda_u241 = androidHandleGatewayAdResponse;
                            androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                            androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                            androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                            androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                            androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                            androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                            androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                            androidHandleGatewayAdResponse$invoke$1.L$7 = tmpAdObject;
                            androidHandleGatewayAdResponse$invoke$1.L$8 = webViewUrl;
                            androidHandleGatewayAdResponse$invoke$1.L$9 = base64ImpressionConfiguration;
                            androidHandleGatewayAdResponse$invoke$1.Z$0 = forceWebViewLoad;
                            androidHandleGatewayAdResponse$invoke$1.J$0 = mark$iv$iv;
                            androidHandleGatewayAdResponse$invoke$1.label = 4;
                            objInvoke = $this$invoke_u24lambda_u242_u24lambda_u241.getWebViewContainerUseCase.invoke($this$invoke_u24lambda_u242_u24lambda_u241.adPlayerScope, tmpAdObject, androidHandleGatewayAdResponse$invoke$1);
                            if (objInvoke == coroutine_suspended) {
                                return coroutine_suspended;
                            }
                            obj = Result.constructor-impl((AndroidWebViewContainer) objInvoke);
                            Object result$iv$iv = Result.box-impl(obj);
                            TimedValue webviewContainerResult = new TimedValue(result$iv$iv, TimeSource$Monotonic$ValueTimeMark.elapsedNow-UwyO8pc(mark$iv$iv), (DefaultConstructorMarker) null);
                            result = ((Result) webviewContainerResult.component1()).unbox-impl();
                            long duration = webviewContainerResult.component2-UwyO8pc();
                            SendDiagnosticEvent sendDiagnosticEvent = this.sendDiagnosticEvent;
                            if (Result.isSuccess-impl(result)) {
                                diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_SUCCESS_TIME;
                            } else {
                                diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_FAILURE_TIME;
                            }
                            SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent, diagnosticEventRequestOuterClass$DiagnosticEventType, Boxing.boxDouble(Duration.toDouble-impl(duration, DurationUnit.MILLISECONDS)), (Map) null, (Map) null, tmpAdObject, (Integer) null, 44, (Object) null);
                            Object obj2 = ((Result) webviewContainerResult.getValue()).unbox-impl();
                            ResultKt.throwOnFailure(obj2);
                            webviewContainer = (AndroidWebViewContainer) obj2;
                            WebViewBridge webviewBridge = this.getWebViewBridge.invoke(webviewContainer, this.adPlayerScope);
                            adPlayer.element = this.getAdPlayer.invoke(webviewBridge, webviewContainer, tmpAdObject, adType);
                            adObject = AdObject.copy$default(tmpAdObject, tmpAdObject.getAdScope(), null, null, null, false, null, null, null, false, null, (AdPlayer) adPlayer.element, null, null, false, null, null, null, null, null, null, tmpAdObject.getWebViewLessLoadingRequiredData(), 1047550, null);
                            FlowKt.launchIn(FlowKt.onEach(this.deviceInfoRepository.getAllowedPii(), new AndroidHandleGatewayAdResponse$invoke$2(adPlayer, null)), ((AdPlayer) adPlayer.element).getScope());
                            loadAdViewerStartedTime = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_STARTED_AD_VIEWER, (Double) null, (Map) null, (Map) null, adObject, (Integer) null, 46, (Object) null);
                            HandleInvocationsFromAdViewer handleInvocationsFromAdViewer = this.getHandleInvocationsFromAdViewer;
                            ByteString adData = response.getAdData();
                            Intrinsics.checkNotNullExpressionValue(adData, "response.adData");
                            String base64$default = ProtobufExtensionsKt.toBase64$default(adData, false, 1, null);
                            ByteString adDataRefreshToken = response.getAdDataRefreshToken();
                            Intrinsics.checkNotNullExpressionValue(adDataRefreshToken, "response.adDataRefreshToken");
                            String base64$default2 = ProtobufExtensionsKt.toBase64$default(adDataRefreshToken, false, 1, null);
                            Intrinsics.checkNotNullExpressionValue(base64ImpressionConfiguration, "base64ImpressionConfiguration");
                            webviewBridge.setExposedFunctions(handleInvocationsFromAdViewer.invoke(base64$default, base64$default2, base64ImpressionConfiguration, adObject));
                            if (forceWebViewLoad || !this.sessionRepository.getNativeConfiguration().getFeatureFlags().getWebviewLessLoadParallelActivityLaunch()) {
                                androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                                androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                                androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                                androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                                androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                                androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                                androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                                androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                                androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                                androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                                androidHandleGatewayAdResponse$invoke$1.label = 5;
                                if (this.loadUrl(tmpAdObject, webViewUrl, webviewContainer, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                                    return coroutine_suspended;
                                }
                                androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                                androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                                androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                                androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                                androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                                androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                                androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                                androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                                androidHandleGatewayAdResponse$invoke$1.label = 6;
                                objSingle = FlowKt.single(((AdPlayer) adPlayer.element).getOnLoadEvent(), androidHandleGatewayAdResponse$invoke$1);
                                if (objSingle == coroutine_suspended) {
                                    return coroutine_suspended;
                                }
                                loadEvent$Completed = (LoadEvent) objSingle;
                            } else {
                                BuildersKt.launch$default(this.adPlayerScope, (CoroutineContext) null, (CoroutineStart) null, new AndroidHandleGatewayAdResponse$invoke$loadEvent$1(this, tmpAdObject, webViewUrl, webviewContainer, null), 3, (Object) null);
                                loadEvent$Completed = LoadEvent$Completed.INSTANCE;
                            }
                            loadEvent = loadEvent$Completed;
                            if (loadEvent instanceof Error) {
                                SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                                this.campaignRepository.setLoadTimestamp(opportunityId);
                                this.adRepository.addAd(opportunityId, adObject);
                                objectId = loadOptions.getObjectId();
                                if (objectId != null || StringsKt.isBlank(objectId)) {
                                    z = true;
                                } else {
                                    z = false;
                                }
                                if (z) {
                                    JSONObject data = loadOptions.getData();
                                    z2 = (data == null || data.has(LegacyLoadUseCase.KEY_AD_MARKUP)) ? false : true;
                                    if (z2) {
                                        this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                    }
                                }
                                return new Success(adObject);
                            }
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                            androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                            androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                            androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                            androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                            androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                            androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                            androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                            androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                            androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                            androidHandleGatewayAdResponse$invoke$1.label = 7;
                            if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                                return coroutine_suspended;
                            }
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                        } catch (Throwable th) {
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "invalid_url", selectedUrl, false, 36, null);
                        }
                        cause = t.getCause();
                        if (cause == null) {
                            throw t;
                        }
                        throw cause;
                    case 1:
                        forceWebViewLoad = androidHandleGatewayAdResponse$invoke$1.Z$1;
                        isHeaderBidding = androidHandleGatewayAdResponse$invoke$1.Z$0;
                        adPlayer = (Ref$ObjectRef) androidHandleGatewayAdResponse$invoke$1.L$6;
                        adType = (DiagnosticEventRequestOuterClass$DiagnosticAdType) androidHandleGatewayAdResponse$invoke$1.L$5;
                        placementId = (String) androidHandleGatewayAdResponse$invoke$1.L$4;
                        response = (AdResponseOuterClass$AdResponse) androidHandleGatewayAdResponse$invoke$1.L$3;
                        opportunityId = (ByteString) androidHandleGatewayAdResponse$invoke$1.L$2;
                        loadOptions = (UnityAdsLoadOptions) androidHandleGatewayAdResponse$invoke$1.L$1;
                        this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        objInvoke2 = $result;
                        webviewConfiguration = (WebViewConfiguration) objInvoke2;
                        adScope = CoroutineScopeKt.plus(this.adPlayerScope, new CoroutineOpportunity(opportunityId));
                        if (forceWebViewLoad) {
                            adObject2 = this.adRepository.getAd(opportunityId);
                            if (adObject2 == null) {
                                return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "webviewless_ad_not_found", null, false, 52, null);
                            }
                        } else {
                            ByteString trackingToken2 = response.getTrackingToken();
                            ByteString byteString3 = opportunityId;
                            String str3 = placementId;
                            Intrinsics.checkNotNullExpressionValue(trackingToken2, HandleInvocationsFromAdViewer.KEY_TRACKING_TOKEN);
                            UnityAdsLoadOptions unityAdsLoadOptions3 = loadOptions;
                            if (isHeaderBidding) {
                                z4 = true;
                            } else {
                                z4 = false;
                            }
                            adObject2 = new AdObject(adScope, byteString3, str3, trackingToken2, false, null, null, null, false, null, null, null, unityAdsLoadOptions3, z4, adType, null, null, null, null, null, null, 2068464, null);
                        }
                        tmpAdObject = adObject2;
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = webviewConfiguration;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = adScope;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = tmpAdObject;
                        androidHandleGatewayAdResponse$invoke$1.Z$0 = isHeaderBidding;
                        androidHandleGatewayAdResponse$invoke$1.Z$1 = forceWebViewLoad;
                        androidHandleGatewayAdResponse$invoke$1.label = 2;
                        if (this.cacheWebViewAssets.invoke(webviewConfiguration, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        if (webviewConfiguration.getEntryPoint().length() == 0) {
                            z3 = true;
                        } else {
                            z3 = false;
                        }
                        if (z3) {
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "no_webview_entry_point", null, false, 52, null);
                        }
                        it = SdkProperties.getConfigUrl();
                        Intrinsics.checkNotNullExpressionValue(it, "it");
                        if (StringsKt.endsWith$default(it, ".html", false, 2, (Object) null)) {
                            entryPoint = it;
                        } else {
                            entryPoint = null;
                        }
                        if (entryPoint == null) {
                            entryPoint = webviewConfiguration.getEntryPoint();
                        }
                        selectedUrl = entryPoint;
                        URI url2 = new URI(selectedUrl);
                        StringBuilder sbAppend2 = new StringBuilder().append("?platform=android&mode=ad-viewer&webviewType=").append(webviewConfiguration.getType()).append('&');
                        query = url2.getQuery();
                        if (query == null) {
                            query = "";
                        }
                        String query3 = sbAppend2.append(query).toString();
                        webViewUrl = StringsKt.substringBeforeLast$default(selectedUrl, "?", (String) null, 2, (Object) null) + query3;
                        if (forceWebViewLoad) {
                            break;
                        }
                        base64ImpressionConfiguration = Base64.encodeToString(response.getImpressionConfiguration().toByteArray(), 2);
                        TimeSource$Monotonic $this$measureTimedValue$iv$iv2 = TimeSource$Monotonic.INSTANCE;
                        mark$iv$iv = $this$measureTimedValue$iv$iv2.markNow-z9LOYto();
                        AndroidHandleGatewayAdResponse androidHandleGatewayAdResponse2 = this;
                        Result$Companion result$Companion2 = Result.Companion;
                        AndroidHandleGatewayAdResponse $this$invoke_u24lambda_u242_u24lambda_u242 = androidHandleGatewayAdResponse2;
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = tmpAdObject;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = webViewUrl;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = base64ImpressionConfiguration;
                        androidHandleGatewayAdResponse$invoke$1.Z$0 = forceWebViewLoad;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = mark$iv$iv;
                        androidHandleGatewayAdResponse$invoke$1.label = 4;
                        objInvoke = $this$invoke_u24lambda_u242_u24lambda_u242.getWebViewContainerUseCase.invoke($this$invoke_u24lambda_u242_u24lambda_u242.adPlayerScope, tmpAdObject, androidHandleGatewayAdResponse$invoke$1);
                        if (objInvoke == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        obj = Result.constructor-impl((AndroidWebViewContainer) objInvoke);
                        Object result$iv$iv2 = Result.box-impl(obj);
                        TimedValue webviewContainerResult2 = new TimedValue(result$iv$iv2, TimeSource$Monotonic$ValueTimeMark.elapsedNow-UwyO8pc(mark$iv$iv), (DefaultConstructorMarker) null);
                        result = ((Result) webviewContainerResult2.component1()).unbox-impl();
                        long duration2 = webviewContainerResult2.component2-UwyO8pc();
                        SendDiagnosticEvent sendDiagnosticEvent2 = this.sendDiagnosticEvent;
                        if (Result.isSuccess-impl(result)) {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_SUCCESS_TIME;
                        } else {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_FAILURE_TIME;
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent2, diagnosticEventRequestOuterClass$DiagnosticEventType, Boxing.boxDouble(Duration.toDouble-impl(duration2, DurationUnit.MILLISECONDS)), (Map) null, (Map) null, tmpAdObject, (Integer) null, 44, (Object) null);
                        Object obj3 = ((Result) webviewContainerResult2.getValue()).unbox-impl();
                        ResultKt.throwOnFailure(obj3);
                        webviewContainer = (AndroidWebViewContainer) obj3;
                        WebViewBridge webviewBridge2 = this.getWebViewBridge.invoke(webviewContainer, this.adPlayerScope);
                        adPlayer.element = this.getAdPlayer.invoke(webviewBridge2, webviewContainer, tmpAdObject, adType);
                        adObject = AdObject.copy$default(tmpAdObject, tmpAdObject.getAdScope(), null, null, null, false, null, null, null, false, null, (AdPlayer) adPlayer.element, null, null, false, null, null, null, null, null, null, tmpAdObject.getWebViewLessLoadingRequiredData(), 1047550, null);
                        FlowKt.launchIn(FlowKt.onEach(this.deviceInfoRepository.getAllowedPii(), new AndroidHandleGatewayAdResponse$invoke$2(adPlayer, null)), ((AdPlayer) adPlayer.element).getScope());
                        loadAdViewerStartedTime = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_STARTED_AD_VIEWER, (Double) null, (Map) null, (Map) null, adObject, (Integer) null, 46, (Object) null);
                        HandleInvocationsFromAdViewer handleInvocationsFromAdViewer2 = this.getHandleInvocationsFromAdViewer;
                        ByteString adData2 = response.getAdData();
                        Intrinsics.checkNotNullExpressionValue(adData2, "response.adData");
                        String base64$default3 = ProtobufExtensionsKt.toBase64$default(adData2, false, 1, null);
                        ByteString adDataRefreshToken2 = response.getAdDataRefreshToken();
                        Intrinsics.checkNotNullExpressionValue(adDataRefreshToken2, "response.adDataRefreshToken");
                        String base64$default4 = ProtobufExtensionsKt.toBase64$default(adDataRefreshToken2, false, 1, null);
                        Intrinsics.checkNotNullExpressionValue(base64ImpressionConfiguration, "base64ImpressionConfiguration");
                        webviewBridge2.setExposedFunctions(handleInvocationsFromAdViewer2.invoke(base64$default3, base64$default4, base64ImpressionConfiguration, adObject));
                        if (forceWebViewLoad) {
                            break;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 5;
                        if (this.loadUrl(tmpAdObject, webViewUrl, webviewContainer, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 6;
                        objSingle = FlowKt.single(((AdPlayer) adPlayer.element).getOnLoadEvent(), androidHandleGatewayAdResponse$invoke$1);
                        if (objSingle == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        loadEvent$Completed = (LoadEvent) objSingle;
                        loadEvent = loadEvent$Completed;
                        if (loadEvent instanceof Error) {
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            this.campaignRepository.setLoadTimestamp(opportunityId);
                            this.adRepository.addAd(opportunityId, adObject);
                            objectId = loadOptions.getObjectId();
                            if (objectId != null) {
                                z = true;
                            } else {
                                z = true;
                            }
                            if (z) {
                                JSONObject data2 = loadOptions.getData();
                                if (data2 == null) {
                                    z2 = false;
                                }
                                if (z2) {
                                    this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                }
                            }
                            return new Success(adObject);
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.label = 7;
                        if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                        cause = t.getCause();
                        if (cause == null) {
                            throw t;
                        }
                        throw cause;
                    case 2:
                        forceWebViewLoad = androidHandleGatewayAdResponse$invoke$1.Z$1;
                        isHeaderBidding = androidHandleGatewayAdResponse$invoke$1.Z$0;
                        tmpAdObject = (AdObject) androidHandleGatewayAdResponse$invoke$1.L$9;
                        adScope = (CoroutineScope) androidHandleGatewayAdResponse$invoke$1.L$8;
                        webviewConfiguration = (WebViewConfiguration) androidHandleGatewayAdResponse$invoke$1.L$7;
                        adPlayer = (Ref$ObjectRef) androidHandleGatewayAdResponse$invoke$1.L$6;
                        adType = (DiagnosticEventRequestOuterClass$DiagnosticAdType) androidHandleGatewayAdResponse$invoke$1.L$5;
                        placementId = (String) androidHandleGatewayAdResponse$invoke$1.L$4;
                        response = (AdResponseOuterClass$AdResponse) androidHandleGatewayAdResponse$invoke$1.L$3;
                        opportunityId = (ByteString) androidHandleGatewayAdResponse$invoke$1.L$2;
                        loadOptions = (UnityAdsLoadOptions) androidHandleGatewayAdResponse$invoke$1.L$1;
                        this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        if (webviewConfiguration.getEntryPoint().length() == 0) {
                            z3 = true;
                        } else {
                            z3 = false;
                        }
                        if (z3) {
                            return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "no_webview_entry_point", null, false, 52, null);
                        }
                        it = SdkProperties.getConfigUrl();
                        Intrinsics.checkNotNullExpressionValue(it, "it");
                        if (StringsKt.endsWith$default(it, ".html", false, 2, (Object) null)) {
                            entryPoint = it;
                        } else {
                            entryPoint = null;
                        }
                        if (entryPoint == null) {
                            entryPoint = webviewConfiguration.getEntryPoint();
                        }
                        selectedUrl = entryPoint;
                        URI url3 = new URI(selectedUrl);
                        StringBuilder sbAppend3 = new StringBuilder().append("?platform=android&mode=ad-viewer&webviewType=").append(webviewConfiguration.getType()).append('&');
                        query = url3.getQuery();
                        if (query == null) {
                            query = "";
                        }
                        String query4 = sbAppend3.append(query).toString();
                        webViewUrl = StringsKt.substringBeforeLast$default(selectedUrl, "?", (String) null, 2, (Object) null) + query4;
                        if (forceWebViewLoad) {
                            break;
                        }
                        base64ImpressionConfiguration = Base64.encodeToString(response.getImpressionConfiguration().toByteArray(), 2);
                        TimeSource$Monotonic $this$measureTimedValue$iv$iv3 = TimeSource$Monotonic.INSTANCE;
                        mark$iv$iv = $this$measureTimedValue$iv$iv3.markNow-z9LOYto();
                        AndroidHandleGatewayAdResponse androidHandleGatewayAdResponse3 = this;
                        Result$Companion result$Companion3 = Result.Companion;
                        AndroidHandleGatewayAdResponse $this$invoke_u24lambda_u242_u24lambda_u243 = androidHandleGatewayAdResponse3;
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adType;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = tmpAdObject;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = webViewUrl;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = base64ImpressionConfiguration;
                        androidHandleGatewayAdResponse$invoke$1.Z$0 = forceWebViewLoad;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = mark$iv$iv;
                        androidHandleGatewayAdResponse$invoke$1.label = 4;
                        objInvoke = $this$invoke_u24lambda_u242_u24lambda_u243.getWebViewContainerUseCase.invoke($this$invoke_u24lambda_u242_u24lambda_u243.adPlayerScope, tmpAdObject, androidHandleGatewayAdResponse$invoke$1);
                        if (objInvoke == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        obj = Result.constructor-impl((AndroidWebViewContainer) objInvoke);
                        Object result$iv$iv3 = Result.box-impl(obj);
                        TimedValue webviewContainerResult3 = new TimedValue(result$iv$iv3, TimeSource$Monotonic$ValueTimeMark.elapsedNow-UwyO8pc(mark$iv$iv), (DefaultConstructorMarker) null);
                        result = ((Result) webviewContainerResult3.component1()).unbox-impl();
                        long duration3 = webviewContainerResult3.component2-UwyO8pc();
                        SendDiagnosticEvent sendDiagnosticEvent3 = this.sendDiagnosticEvent;
                        if (Result.isSuccess-impl(result)) {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_SUCCESS_TIME;
                        } else {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_FAILURE_TIME;
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent3, diagnosticEventRequestOuterClass$DiagnosticEventType, Boxing.boxDouble(Duration.toDouble-impl(duration3, DurationUnit.MILLISECONDS)), (Map) null, (Map) null, tmpAdObject, (Integer) null, 44, (Object) null);
                        Object obj4 = ((Result) webviewContainerResult3.getValue()).unbox-impl();
                        ResultKt.throwOnFailure(obj4);
                        webviewContainer = (AndroidWebViewContainer) obj4;
                        WebViewBridge webviewBridge3 = this.getWebViewBridge.invoke(webviewContainer, this.adPlayerScope);
                        adPlayer.element = this.getAdPlayer.invoke(webviewBridge3, webviewContainer, tmpAdObject, adType);
                        adObject = AdObject.copy$default(tmpAdObject, tmpAdObject.getAdScope(), null, null, null, false, null, null, null, false, null, (AdPlayer) adPlayer.element, null, null, false, null, null, null, null, null, null, tmpAdObject.getWebViewLessLoadingRequiredData(), 1047550, null);
                        FlowKt.launchIn(FlowKt.onEach(this.deviceInfoRepository.getAllowedPii(), new AndroidHandleGatewayAdResponse$invoke$2(adPlayer, null)), ((AdPlayer) adPlayer.element).getScope());
                        loadAdViewerStartedTime = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_STARTED_AD_VIEWER, (Double) null, (Map) null, (Map) null, adObject, (Integer) null, 46, (Object) null);
                        HandleInvocationsFromAdViewer handleInvocationsFromAdViewer3 = this.getHandleInvocationsFromAdViewer;
                        ByteString adData3 = response.getAdData();
                        Intrinsics.checkNotNullExpressionValue(adData3, "response.adData");
                        String base64$default5 = ProtobufExtensionsKt.toBase64$default(adData3, false, 1, null);
                        ByteString adDataRefreshToken3 = response.getAdDataRefreshToken();
                        Intrinsics.checkNotNullExpressionValue(adDataRefreshToken3, "response.adDataRefreshToken");
                        String base64$default6 = ProtobufExtensionsKt.toBase64$default(adDataRefreshToken3, false, 1, null);
                        Intrinsics.checkNotNullExpressionValue(base64ImpressionConfiguration, "base64ImpressionConfiguration");
                        webviewBridge3.setExposedFunctions(handleInvocationsFromAdViewer3.invoke(base64$default5, base64$default6, base64ImpressionConfiguration, adObject));
                        if (forceWebViewLoad) {
                            break;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 5;
                        if (this.loadUrl(tmpAdObject, webViewUrl, webviewContainer, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 6;
                        objSingle = FlowKt.single(((AdPlayer) adPlayer.element).getOnLoadEvent(), androidHandleGatewayAdResponse$invoke$1);
                        if (objSingle == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        loadEvent$Completed = (LoadEvent) objSingle;
                        loadEvent = loadEvent$Completed;
                        if (loadEvent instanceof Error) {
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            this.campaignRepository.setLoadTimestamp(opportunityId);
                            this.adRepository.addAd(opportunityId, adObject);
                            objectId = loadOptions.getObjectId();
                            if (objectId != null) {
                                z = true;
                            } else {
                                z = true;
                            }
                            if (z) {
                                JSONObject data3 = loadOptions.getData();
                                if (data3 == null) {
                                    z2 = false;
                                }
                                if (z2) {
                                    this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                }
                            }
                            return new Success(adObject);
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.label = 7;
                        if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                        cause = t.getCause();
                        if (cause == null) {
                            throw t;
                        }
                        throw cause;
                    case 3:
                        ResultKt.throwOnFailure($result);
                        return $result;
                    case 4:
                        mark$iv$iv = androidHandleGatewayAdResponse$invoke$1.J$0;
                        forceWebViewLoad = androidHandleGatewayAdResponse$invoke$1.Z$0;
                        base64ImpressionConfiguration = (String) androidHandleGatewayAdResponse$invoke$1.L$9;
                        webViewUrl = (String) androidHandleGatewayAdResponse$invoke$1.L$8;
                        tmpAdObject = (AdObject) androidHandleGatewayAdResponse$invoke$1.L$7;
                        adPlayer = (Ref$ObjectRef) androidHandleGatewayAdResponse$invoke$1.L$6;
                        adType = (DiagnosticEventRequestOuterClass$DiagnosticAdType) androidHandleGatewayAdResponse$invoke$1.L$5;
                        placementId = (String) androidHandleGatewayAdResponse$invoke$1.L$4;
                        response = (AdResponseOuterClass$AdResponse) androidHandleGatewayAdResponse$invoke$1.L$3;
                        opportunityId = (ByteString) androidHandleGatewayAdResponse$invoke$1.L$2;
                        loadOptions = (UnityAdsLoadOptions) androidHandleGatewayAdResponse$invoke$1.L$1;
                        this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        objInvoke = $result;
                        obj = Result.constructor-impl((AndroidWebViewContainer) objInvoke);
                        Object result$iv$iv4 = Result.box-impl(obj);
                        TimedValue webviewContainerResult4 = new TimedValue(result$iv$iv4, TimeSource$Monotonic$ValueTimeMark.elapsedNow-UwyO8pc(mark$iv$iv), (DefaultConstructorMarker) null);
                        result = ((Result) webviewContainerResult4.component1()).unbox-impl();
                        long duration4 = webviewContainerResult4.component2-UwyO8pc();
                        SendDiagnosticEvent sendDiagnosticEvent4 = this.sendDiagnosticEvent;
                        if (Result.isSuccess-impl(result)) {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_SUCCESS_TIME;
                        } else {
                            diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_WEBVIEW_FAILURE_TIME;
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent4, diagnosticEventRequestOuterClass$DiagnosticEventType, Boxing.boxDouble(Duration.toDouble-impl(duration4, DurationUnit.MILLISECONDS)), (Map) null, (Map) null, tmpAdObject, (Integer) null, 44, (Object) null);
                        Object obj5 = ((Result) webviewContainerResult4.getValue()).unbox-impl();
                        ResultKt.throwOnFailure(obj5);
                        webviewContainer = (AndroidWebViewContainer) obj5;
                        WebViewBridge webviewBridge4 = this.getWebViewBridge.invoke(webviewContainer, this.adPlayerScope);
                        adPlayer.element = this.getAdPlayer.invoke(webviewBridge4, webviewContainer, tmpAdObject, adType);
                        adObject = AdObject.copy$default(tmpAdObject, tmpAdObject.getAdScope(), null, null, null, false, null, null, null, false, null, (AdPlayer) adPlayer.element, null, null, false, null, null, null, null, null, null, tmpAdObject.getWebViewLessLoadingRequiredData(), 1047550, null);
                        FlowKt.launchIn(FlowKt.onEach(this.deviceInfoRepository.getAllowedPii(), new AndroidHandleGatewayAdResponse$invoke$2(adPlayer, null)), ((AdPlayer) adPlayer.element).getScope());
                        loadAdViewerStartedTime = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_STARTED_AD_VIEWER, (Double) null, (Map) null, (Map) null, adObject, (Integer) null, 46, (Object) null);
                        HandleInvocationsFromAdViewer handleInvocationsFromAdViewer4 = this.getHandleInvocationsFromAdViewer;
                        ByteString adData4 = response.getAdData();
                        Intrinsics.checkNotNullExpressionValue(adData4, "response.adData");
                        String base64$default7 = ProtobufExtensionsKt.toBase64$default(adData4, false, 1, null);
                        ByteString adDataRefreshToken4 = response.getAdDataRefreshToken();
                        Intrinsics.checkNotNullExpressionValue(adDataRefreshToken4, "response.adDataRefreshToken");
                        String base64$default8 = ProtobufExtensionsKt.toBase64$default(adDataRefreshToken4, false, 1, null);
                        Intrinsics.checkNotNullExpressionValue(base64ImpressionConfiguration, "base64ImpressionConfiguration");
                        webviewBridge4.setExposedFunctions(handleInvocationsFromAdViewer4.invoke(base64$default7, base64$default8, base64ImpressionConfiguration, adObject));
                        if (forceWebViewLoad) {
                            break;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 5;
                        if (this.loadUrl(tmpAdObject, webViewUrl, webviewContainer, androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 6;
                        objSingle = FlowKt.single(((AdPlayer) adPlayer.element).getOnLoadEvent(), androidHandleGatewayAdResponse$invoke$1);
                        if (objSingle == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        loadEvent$Completed = (LoadEvent) objSingle;
                        loadEvent = loadEvent$Completed;
                        if (loadEvent instanceof Error) {
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            this.campaignRepository.setLoadTimestamp(opportunityId);
                            this.adRepository.addAd(opportunityId, adObject);
                            objectId = loadOptions.getObjectId();
                            if (objectId != null) {
                                z = true;
                            } else {
                                z = true;
                            }
                            if (z) {
                                JSONObject data4 = loadOptions.getData();
                                if (data4 == null) {
                                    z2 = false;
                                }
                                if (z2) {
                                    this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                }
                            }
                            return new Success(adObject);
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.label = 7;
                        if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                    case 5:
                        loadAdViewerStartedTime = androidHandleGatewayAdResponse$invoke$1.J$0;
                        adObject = (AdObject) androidHandleGatewayAdResponse$invoke$1.L$6;
                        adPlayer = (Ref$ObjectRef) androidHandleGatewayAdResponse$invoke$1.L$5;
                        placementId = (String) androidHandleGatewayAdResponse$invoke$1.L$4;
                        response = (AdResponseOuterClass$AdResponse) androidHandleGatewayAdResponse$invoke$1.L$3;
                        opportunityId = (ByteString) androidHandleGatewayAdResponse$invoke$1.L$2;
                        loadOptions = (UnityAdsLoadOptions) androidHandleGatewayAdResponse$invoke$1.L$1;
                        this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = loadOptions;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = placementId;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.J$0 = loadAdViewerStartedTime;
                        androidHandleGatewayAdResponse$invoke$1.label = 6;
                        objSingle = FlowKt.single(((AdPlayer) adPlayer.element).getOnLoadEvent(), androidHandleGatewayAdResponse$invoke$1);
                        if (objSingle == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        loadEvent$Completed = (LoadEvent) objSingle;
                        loadEvent = loadEvent$Completed;
                        if (loadEvent instanceof Error) {
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            this.campaignRepository.setLoadTimestamp(opportunityId);
                            this.adRepository.addAd(opportunityId, adObject);
                            objectId = loadOptions.getObjectId();
                            if (objectId != null) {
                                z = true;
                            } else {
                                z = true;
                            }
                            if (z) {
                                JSONObject data5 = loadOptions.getData();
                                if (data5 == null) {
                                    z2 = false;
                                }
                                if (z2) {
                                    this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                }
                            }
                            return new Success(adObject);
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.label = 7;
                        if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                    case 6:
                        loadAdViewerStartedTime = androidHandleGatewayAdResponse$invoke$1.J$0;
                        adObject = (AdObject) androidHandleGatewayAdResponse$invoke$1.L$6;
                        adPlayer = (Ref$ObjectRef) androidHandleGatewayAdResponse$invoke$1.L$5;
                        placementId = (String) androidHandleGatewayAdResponse$invoke$1.L$4;
                        response = (AdResponseOuterClass$AdResponse) androidHandleGatewayAdResponse$invoke$1.L$3;
                        opportunityId = (ByteString) androidHandleGatewayAdResponse$invoke$1.L$2;
                        loadOptions = (UnityAdsLoadOptions) androidHandleGatewayAdResponse$invoke$1.L$1;
                        this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        objSingle = $result;
                        loadEvent$Completed = (LoadEvent) objSingle;
                        loadEvent = loadEvent$Completed;
                        if (loadEvent instanceof Error) {
                            SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_SUCCESS_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                            this.campaignRepository.setLoadTimestamp(opportunityId);
                            this.adRepository.addAd(opportunityId, adObject);
                            objectId = loadOptions.getObjectId();
                            if (objectId != null) {
                                z = true;
                            } else {
                                z = true;
                            }
                            if (z) {
                                JSONObject data6 = loadOptions.getData();
                                if (data6 == null) {
                                    z2 = false;
                                }
                                if (z2) {
                                    this.adRepository.enqueueOpportunityForPlacement(placementId, opportunityId);
                                }
                            }
                            return new Success(adObject);
                        }
                        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_CREATE_AD_OBJECT_FAILURE_TIME, Boxing.boxDouble(TimeExtensionsKt.elapsedMillis(TimeSource$Monotonic$ValueTimeMark.box-impl(loadAdViewerStartedTime))), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
                        androidHandleGatewayAdResponse$invoke$1.L$0 = this;
                        androidHandleGatewayAdResponse$invoke$1.L$1 = opportunityId;
                        androidHandleGatewayAdResponse$invoke$1.L$2 = response;
                        androidHandleGatewayAdResponse$invoke$1.L$3 = adPlayer;
                        androidHandleGatewayAdResponse$invoke$1.L$4 = adObject;
                        androidHandleGatewayAdResponse$invoke$1.L$5 = loadEvent;
                        androidHandleGatewayAdResponse$invoke$1.L$6 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$7 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$8 = null;
                        androidHandleGatewayAdResponse$invoke$1.L$9 = null;
                        androidHandleGatewayAdResponse$invoke$1.label = 7;
                        if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$3(this, loadEvent, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                            return coroutine_suspended;
                        }
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                    case 7:
                        loadEvent = (LoadEvent) androidHandleGatewayAdResponse$invoke$1.L$5;
                        adObject = (AdObject) androidHandleGatewayAdResponse$invoke$1.L$4;
                        ResultKt.throwOnFailure($result);
                        return new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, null, "adviewer", ((Error) loadEvent).getMessage(), adObject.isScarAd(), 4, null);
                    case 8:
                        t = (CancellationException) androidHandleGatewayAdResponse$invoke$1.L$0;
                        ResultKt.throwOnFailure($result);
                        cause = t.getCause();
                        if (cause == null) {
                            throw t;
                        }
                        throw cause;
                    default:
                        throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                }
            } catch (Throwable th2) {
                Result$Companion result$Companion4 = Result.Companion;
                obj = Result.constructor-impl(ResultKt.createFailure(th2));
            }
        } catch (CancellationException e) {
            t = e;
            androidHandleGatewayAdResponse$invoke$1.L$0 = t;
            androidHandleGatewayAdResponse$invoke$1.L$1 = null;
            androidHandleGatewayAdResponse$invoke$1.L$2 = null;
            androidHandleGatewayAdResponse$invoke$1.L$3 = null;
            androidHandleGatewayAdResponse$invoke$1.L$4 = null;
            androidHandleGatewayAdResponse$invoke$1.L$5 = null;
            androidHandleGatewayAdResponse$invoke$1.L$6 = null;
            androidHandleGatewayAdResponse$invoke$1.L$7 = null;
            androidHandleGatewayAdResponse$invoke$1.L$8 = null;
            androidHandleGatewayAdResponse$invoke$1.L$9 = null;
            androidHandleGatewayAdResponse$invoke$1.label = 8;
            if (BuildersKt.withContext(NonCancellable.INSTANCE, new AndroidHandleGatewayAdResponse$invoke$4(this, t, opportunityId, response, adPlayer, null), androidHandleGatewayAdResponse$invoke$1) == coroutine_suspended) {
                return coroutine_suspended;
            }
        }
    }

    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    private final Object loadUrl(AdObject adObject, String webViewUrl, WebViewContainer webviewContainer, Continuation<? super Unit> continuation) {
        AndroidHandleGatewayAdResponse$loadUrl$1 androidHandleGatewayAdResponse$loadUrl$1;
        Object obj;
        long mark$iv$iv;
        if (continuation instanceof AndroidHandleGatewayAdResponse$loadUrl$1) {
            androidHandleGatewayAdResponse$loadUrl$1 = (AndroidHandleGatewayAdResponse$loadUrl$1) continuation;
            if ((androidHandleGatewayAdResponse$loadUrl$1.label & Integer.MIN_VALUE) != 0) {
                androidHandleGatewayAdResponse$loadUrl$1.label -= Integer.MIN_VALUE;
            } else {
                androidHandleGatewayAdResponse$loadUrl$1 = new AndroidHandleGatewayAdResponse$loadUrl$1(this, continuation);
            }
        } else {
            androidHandleGatewayAdResponse$loadUrl$1 = new AndroidHandleGatewayAdResponse$loadUrl$1(this, continuation);
        }
        Object $result = androidHandleGatewayAdResponse$loadUrl$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        try {
            switch (androidHandleGatewayAdResponse$loadUrl$1.label) {
                case 0:
                    ResultKt.throwOnFailure($result);
                    TimeSource$Monotonic $this$measureTimedValue$iv$iv = TimeSource$Monotonic.INSTANCE;
                    mark$iv$iv = $this$measureTimedValue$iv$iv.markNow-z9LOYto();
                    Result$Companion result$Companion = Result.Companion;
                    AndroidHandleGatewayAdResponse androidHandleGatewayAdResponse = this;
                    androidHandleGatewayAdResponse$loadUrl$1.L$0 = this;
                    androidHandleGatewayAdResponse$loadUrl$1.L$1 = adObject;
                    androidHandleGatewayAdResponse$loadUrl$1.J$0 = mark$iv$iv;
                    androidHandleGatewayAdResponse$loadUrl$1.label = 1;
                    if (webviewContainer.loadUrl(webViewUrl, androidHandleGatewayAdResponse$loadUrl$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    break;
                case 1:
                    mark$iv$iv = androidHandleGatewayAdResponse$loadUrl$1.J$0;
                    adObject = (AdObject) androidHandleGatewayAdResponse$loadUrl$1.L$1;
                    this = (AndroidHandleGatewayAdResponse) androidHandleGatewayAdResponse$loadUrl$1.L$0;
                    ResultKt.throwOnFailure($result);
                    break;
                default:
                    throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }
            obj = Result.constructor-impl(Unit.INSTANCE);
        } catch (Throwable th) {
            Result$Companion result$Companion2 = Result.Companion;
            obj = Result.constructor-impl(ResultKt.createFailure(th));
        }
        Object result$iv$iv = Result.box-impl(obj);
        TimedValue timedValue = new TimedValue(result$iv$iv, TimeSource$Monotonic$ValueTimeMark.elapsedNow-UwyO8pc(mark$iv$iv), (DefaultConstructorMarker) null);
        Object result = ((Result) timedValue.component1()).unbox-impl();
        long duration = timedValue.component2-UwyO8pc();
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, Result.isSuccess-impl(result) ? DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_FILE_SUCCESS_TIME : DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_FILE_FAILURE_TIME, Boxing.boxDouble(Duration.toDouble-impl(duration, DurationUnit.MILLISECONDS)), (Map) null, (Map) null, adObject, (Integer) null, 44, (Object) null);
        ResultKt.throwOnFailure(result);
        return Unit.INSTANCE;
    }

    /* JADX WARN: Code duplicated, block: B:15:0x00a2  */
    /* JADX WARN: Code duplicated, block: B:17:0x00ab  */
    /* JADX WARN: Code duplicated, block: B:25:0x011b  */
    /* JADX WARN: Code duplicated, block: B:27:0x0134  */
    /* JADX WARN: Code duplicated, block: B:32:0x0143  */
    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    private final Object cleanup(Throwable t, ByteString opportunityId, AdResponseOuterClass$AdResponse response, AdPlayer adPlayer, Continuation<? super Unit> continuation) {
        AndroidHandleGatewayAdResponse$cleanup$1 androidHandleGatewayAdResponse$cleanup$1;
        AdPlayer adPlayer2;
        String message;
        if (continuation instanceof AndroidHandleGatewayAdResponse$cleanup$1) {
            androidHandleGatewayAdResponse$cleanup$1 = (AndroidHandleGatewayAdResponse$cleanup$1) continuation;
            if ((androidHandleGatewayAdResponse$cleanup$1.label & Integer.MIN_VALUE) != 0) {
                androidHandleGatewayAdResponse$cleanup$1.label -= Integer.MIN_VALUE;
            } else {
                androidHandleGatewayAdResponse$cleanup$1 = new AndroidHandleGatewayAdResponse$cleanup$1(this, continuation);
            }
        } else {
            androidHandleGatewayAdResponse$cleanup$1 = new AndroidHandleGatewayAdResponse$cleanup$1(this, continuation);
        }
        Object $result = androidHandleGatewayAdResponse$cleanup$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        switch (androidHandleGatewayAdResponse$cleanup$1.label) {
            case 0:
                ResultKt.throwOnFailure($result);
                OperativeEventErrorDataKt$Dsl$Companion operativeEventErrorDataKt$Dsl$Companion = OperativeEventErrorDataKt$Dsl.Companion;
                OperativeEventRequestOuterClass$OperativeEventErrorData$Builder operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder = OperativeEventRequestOuterClass$OperativeEventErrorData.newBuilder();
                Intrinsics.checkNotNullExpressionValue(operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder, "newBuilder()");
                OperativeEventErrorDataKt$Dsl $this$operativeEventErrorData_u24lambda_u240$iv = operativeEventErrorDataKt$Dsl$Companion._create(operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder);
                $this$operativeEventErrorData_u24lambda_u240$iv.setErrorType(OperativeEventRequestOuterClass$OperativeEventErrorType.OPERATIVE_EVENT_ERROR_TYPE_UNSPECIFIED);
                Throwable cause = t.getCause();
                if (cause != null) {
                    message = cause.getMessage();
                    if (message == null) {
                        message = t.getMessage();
                        if (message == null) {
                            message = "";
                        }
                    }
                } else {
                    message = t.getMessage();
                    if (message == null) {
                        message = "";
                    }
                }
                $this$operativeEventErrorData_u24lambda_u240$iv.setMessage(message);
                OperativeEventRequestOuterClass$OperativeEventErrorData operativeEventErrorData = $this$operativeEventErrorData_u24lambda_u240$iv._build();
                GetOperativeEventApi getOperativeEventApi = this.getOperativeEventApi;
                OperativeEventRequestOuterClass$OperativeEventType operativeEventRequestOuterClass$OperativeEventType = OperativeEventRequestOuterClass$OperativeEventType.OPERATIVE_EVENT_TYPE_LOAD_ERROR;
                ByteString trackingToken = response.getTrackingToken();
                Intrinsics.checkNotNullExpressionValue(trackingToken, "response.trackingToken");
                ByteString byteString = operativeEventErrorData.toByteString();
                Intrinsics.checkNotNullExpressionValue(byteString, "operativeEventErrorData.toByteString()");
                androidHandleGatewayAdResponse$cleanup$1.L$0 = adPlayer;
                androidHandleGatewayAdResponse$cleanup$1.label = 1;
                if (GetOperativeEventApi.invoke$default(getOperativeEventApi, operativeEventRequestOuterClass$OperativeEventType, opportunityId, trackingToken, byteString, null, null, androidHandleGatewayAdResponse$cleanup$1, 48, null) == coroutine_suspended) {
                    return coroutine_suspended;
                }
                adPlayer2 = adPlayer;
                if (adPlayer2 != null) {
                    return Unit.INSTANCE;
                }
                androidHandleGatewayAdResponse$cleanup$1.L$0 = null;
                androidHandleGatewayAdResponse$cleanup$1.label = 2;
                if (adPlayer2.destroy(androidHandleGatewayAdResponse$cleanup$1) == coroutine_suspended) {
                    return coroutine_suspended;
                }
                return Unit.INSTANCE;
            case 1:
                adPlayer = (AdPlayer) androidHandleGatewayAdResponse$cleanup$1.L$0;
                ResultKt.throwOnFailure($result);
                adPlayer2 = adPlayer;
                if (adPlayer2 != null) {
                    return Unit.INSTANCE;
                }
                androidHandleGatewayAdResponse$cleanup$1.L$0 = null;
                androidHandleGatewayAdResponse$cleanup$1.label = 2;
                if (adPlayer2.destroy(androidHandleGatewayAdResponse$cleanup$1) == coroutine_suspended) {
                    return coroutine_suspended;
                }
                return Unit.INSTANCE;
            case 2:
                ResultKt.throwOnFailure($result);
                return Unit.INSTANCE;
            default:
                throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
        }
    }
}