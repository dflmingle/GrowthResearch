package com.unity3d.ads.core.domain;

import com.google.protobuf.ByteString;
import com.unity3d.ads.UnityAds$UnityAdsShowError;
import com.unity3d.ads.UnityAdsShowOptions;
import com.unity3d.ads.adplayer.AdPlayer;
import com.unity3d.ads.adplayer.EmbeddableAdPlayer;
import com.unity3d.ads.adplayer.model.ShowStatus;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.model.AdObjectState;
import com.unity3d.ads.core.data.model.InitializationState;
import com.unity3d.ads.core.data.model.Listeners;
import com.unity3d.ads.core.data.model.LoadResult;
import com.unity3d.ads.core.data.model.OperationType;
import com.unity3d.ads.core.data.repository.AdRepository;
import com.unity3d.ads.core.data.repository.SessionRepository;
import com.unity3d.ads.core.domain.events.GetOperativeEventApi;
import com.unity3d.ads.core.extensions.FlowExtensionsKt;
import com.unity3d.ads.core.extensions.ProtobufExtensionsKt;
import com.unity3d.ads.core.extensions.TimeExtensionsKt;
import com.unity3d.ads.core.log.Logger;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.OperativeEventErrorDataKt$Dsl;
import gatewayprotocol.v1.OperativeEventErrorDataKt$Dsl$Companion;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorData;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorData$Builder;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventErrorType;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventType;
import java.util.Arrays;
import java.util.Map;
import java.util.UUID;
import kotlin.Metadata;
import kotlin.Pair;
import kotlin.Result;
import kotlin.Result$Companion;
import kotlin.ResultKt;
import kotlin.TuplesKt;
import kotlin.Unit;
import kotlin.collections.MapsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function6;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.Ref$BooleanRef;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.time.TimeMark;
import kotlin.time.TimeSource$Monotonic;
import kotlin.time.TimeSource$Monotonic$ValueTimeMark;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.CoroutineScopeKt;
import kotlinx.coroutines.flow.Flow;
import kotlinx.coroutines.flow.FlowKt;
import kotlinx.coroutines.flow.MutableStateFlow;
import kotlinx.coroutines.flow.StateFlowKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.json.JSONObject;

/* JADX INFO: compiled from: LegacyShowUseCase.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/LegacyShowUseCase.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000\u009e\u0001\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010$\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\t\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0006\b\u0000\u0018\u0000 E2\u00020\u0001:\u0001EBE\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\t\u0012\u0006\u0010\n\u001a\u00020\u000b\u0012\u0006\u0010\f\u001a\u00020\r\u0012\u0006\u0010\u000e\u001a\u00020\u000f\u0012\u0006\u0010\u0010\u001a\u00020\u0011¢\u0006\u0002\u0010\u0012J \u0010\u001d\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010!\u001a\u00020\"H\u0002J\u0010\u0010#\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 H\u0002J\b\u0010$\u001a\u00020\u0019H\u0002J\u0012\u0010%\u001a\u0004\u0018\u00010\u00192\u0006\u0010\u001b\u001a\u00020\u001cH\u0002J?\u0010&\u001a\u000e\u0012\u0004\u0012\u00020\u0019\u0012\u0004\u0012\u00020\u00190'2\u0006\u0010(\u001a\u00020\u00192\b\u0010)\u001a\u0004\u0018\u00010*2\b\u0010+\u001a\u0004\u0018\u00010\u00192\b\u0010,\u001a\u0004\u0018\u00010\u001cH\u0002¢\u0006\u0002\u0010-J\u0010\u0010.\u001a\u00020\u00142\u0006\u0010/\u001a\u00020\u0019H\u0002J-\u00100\u001a\u00020\u001e2\b\u0010\u0018\u001a\u0004\u0018\u00010\u00192\b\u0010\u001b\u001a\u0004\u0018\u00010\u001c2\u0006\u0010!\u001a\u00020\"H\u0086Bø\u0001\u0000¢\u0006\u0002\u00101J)\u00102\u001a\u00020\u001e2\u0006\u00103\u001a\u0002042\u0006\u00105\u001a\u00020\u00192\u0006\u0010\u0013\u001a\u00020\u0014H\u0082@ø\u0001\u0000¢\u0006\u0002\u00106J \u00107\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010!\u001a\u00020\"H\u0002JJ\u00108\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u00109\u001a\u00020:2\u0006\u0010!\u001a\u00020\"2\n\b\u0002\u0010;\u001a\u0004\u0018\u00010\u00192\n\b\u0002\u0010<\u001a\u0004\u0018\u00010\u00192\b\u0010,\u001a\u0004\u0018\u00010\u001cH\u0002Jr\u0010=\u001a:\b\u0001\u0012\u0004\u0012\u00020\u0019\u0012\u0004\u0012\u00020?\u0012\u0004\u0012\u00020\u0019\u0012\u0006\u0012\u0004\u0018\u00010*\u0012\u0006\u0012\u0004\u0018\u00010\u0019\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u001e0@\u0012\u0006\u0012\u0004\u0018\u00010\u00010>2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010/\u001a\u00020\u00192\u0006\u0010!\u001a\u00020\"2\b\u0010,\u001a\u0004\u0018\u00010\u001cH\u0002ø\u0001\u0000¢\u0006\u0002\u0010AJ\u001e\u0010B\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010!\u001a\u00020\"J\u001a\u0010C\u001a\u00020\u001e2\u0006\u0010/\u001a\u00020\u00192\b\u0010,\u001a\u0004\u0018\u00010\u001cH\u0002J \u0010D\u001a\u00020\u001e2\u0006\u0010\u001f\u001a\u00020 2\u0006\u0010\u0018\u001a\u00020\u00192\u0006\u0010!\u001a\u00020\"H\u0002R\u0010\u0010\u0013\u001a\u0004\u0018\u00010\u0014X\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\u0015\u001a\b\u0012\u0004\u0012\u00020\u00170\u0016X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0010\u001a\u00020\u0011X\u0082\u0004¢\u0006\u0002\n\u0000R\u0010\u0010\u0018\u001a\u0004\u0018\u00010\u0019X\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\f\u001a\u00020\rX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\u001a\u001a\b\u0012\u0004\u0012\u00020\u00170\u0016X\u0082\u0004¢\u0006\u0002\n\u0000R\u0010\u0010\u001b\u001a\u0004\u0018\u00010\u001cX\u0082\u000e¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006F"}, d2 = {"Lcom/unity3d/ads/core/domain/LegacyShowUseCase;", "", "show", "Lcom/unity3d/ads/core/domain/Show;", "adRepository", "Lcom/unity3d/ads/core/data/repository/AdRepository;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "getOperativeEventApi", "Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;", "getInitializationState", "Lcom/unity3d/ads/core/domain/GetInitializationState;", "sessionRepository", "Lcom/unity3d/ads/core/data/repository/SessionRepository;", "safeCallbackInvoke", "Lcom/unity3d/ads/core/domain/SafeCallbackInvoke;", "logger", "Lcom/unity3d/ads/core/log/Logger;", "(Lcom/unity3d/ads/core/domain/Show;Lcom/unity3d/ads/core/data/repository/AdRepository;Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;Lcom/unity3d/ads/core/domain/GetInitializationState;Lcom/unity3d/ads/core/data/repository/SessionRepository;Lcom/unity3d/ads/core/domain/SafeCallbackInvoke;Lcom/unity3d/ads/core/log/Logger;)V", "adObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "hasStarted", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "placement", "", "timeoutCancellationRequested", "unityAdsShowOptions", "Lcom/unity3d/ads/UnityAdsShowOptions;", "bannerLeftApplication", "", "startTime", "Lkotlin/time/TimeMark;", "listeners", "Lcom/unity3d/ads/core/data/model/Listeners;", "cancelTimeout", "getAdInfoString", "getOpportunityId", "getTags", "", "diagnosticReason", "code", "", "debugMessage", "showOptions", "(Ljava/lang/String;Ljava/lang/Integer;Ljava/lang/String;Lcom/unity3d/ads/UnityAdsShowOptions;)Ljava/util/Map;", "getTmpAdObject", "opportunityId", "invoke", "(Ljava/lang/String;Lcom/unity3d/ads/UnityAdsShowOptions;Lcom/unity3d/ads/core/data/model/Listeners;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "sendOperativeError", "operativeEvent", "Lgatewayprotocol/v1/OperativeEventRequestOuterClass$OperativeEventErrorType;", "operativeMessage", "(Lgatewayprotocol/v1/OperativeEventRequestOuterClass$OperativeEventErrorType;Ljava/lang/String;Lcom/unity3d/ads/core/data/model/AdObject;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "showClicked", "showCompleted", "status", "Lcom/unity3d/ads/adplayer/model/ShowStatus;", "reason", "reasonDebug", "showError", "Lkotlin/Function6;", "Lcom/unity3d/ads/UnityAds$UnityAdsShowError;", "Lkotlin/coroutines/Continuation;", "(Lkotlin/time/TimeMark;Ljava/lang/String;Ljava/lang/String;Lcom/unity3d/ads/core/data/model/Listeners;Lcom/unity3d/ads/UnityAdsShowOptions;)Lkotlin/jvm/functions/Function6;", "showReceivedReward", "showStart", "showStarted", "Companion", "unity-ads_defaultRelease"})
@SourceDebugExtension({"SMAP\nLegacyShowUseCase.kt\nKotlin\n*S Kotlin\n*F\n+ 1 LegacyShowUseCase.kt\ncom/unity3d/ads/core/domain/LegacyShowUseCase\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n+ 3 OperativeEventErrorDataKt.kt\ngatewayprotocol/v1/OperativeEventErrorDataKtKt\n*L\n1#1,409:1\n1#2:410\n1#2:412\n10#3:411\n*S KotlinDebug\n*F\n+ 1 LegacyShowUseCase.kt\ncom/unity3d/ads/core/domain/LegacyShowUseCase\n*L\n270#1:412\n270#1:411\n*E\n"})
public final class LegacyShowUseCase {

    @NotNull
    public static final LegacyShowUseCase$Companion Companion = new LegacyShowUseCase$Companion(null);

    @NotNull
    private final Show show;

    @NotNull
    private final AdRepository adRepository;

    @NotNull
    private final SendDiagnosticEvent sendDiagnosticEvent;

    @NotNull
    private final GetOperativeEventApi getOperativeEventApi;

    @NotNull
    private final GetInitializationState getInitializationState;

    @NotNull
    private final SessionRepository sessionRepository;

    @NotNull
    private final SafeCallbackInvoke safeCallbackInvoke;

    @NotNull
    private final Logger logger;

    @NotNull
    private final MutableStateFlow<Boolean> hasStarted;

    @NotNull
    private final MutableStateFlow<Boolean> timeoutCancellationRequested;

    @Nullable
    private AdObject adObject;

    @Nullable
    private String placement;

    @Nullable
    private UnityAdsShowOptions unityAdsShowOptions;

    @NotNull
    public static final String KEY_OBJECT_ID = "objectId";

    @NotNull
    public static final String MESSAGE_PLACEMENT_NOT_LOADED = "Placement %s must be Loaded before calling Show";

    @NotNull
    public static final String MESSAGE_OPPORTUNITY_ID = "No valid opportunity id provided";

    @NotNull
    public static final String MESSAGE_NO_AD_OBJECT = "No ad object found for opportunity id: ";

    @NotNull
    public static final String MESSAGE_ALREADY_SHOWING = "Can't show a new ad unit when ad unit is already open";

    @NotNull
    public static final String MESSAGE_TIMEOUT = "[UnityAds] Timeout while trying to show ";

    @NotNull
    public static final String MESSAGE_AD_OBJECT_EXPIRED = "The ad has expired";

    @NotNull
    public static final String MSG_OPPORTUNITY_AND_PLACEMENT_NOT_MATCHING = "[UnityAds] Object ID and Placement ID provided does not match previously loaded ad";

    @NotNull
    public static final String MESSAGE_OPT_TIMEOUT = "timeout";

    @NotNull
    public static final String MESSAGE_AD_PLAYER_UNAVAILABLE = "Ad player is unavailable.";
    private static volatile boolean isFullscreenAdShowing;

    public LegacyShowUseCase(@NotNull Show show, @NotNull AdRepository adRepository, @NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull GetOperativeEventApi getOperativeEventApi, @NotNull GetInitializationState getInitializationState, @NotNull SessionRepository sessionRepository, @NotNull SafeCallbackInvoke safeCallbackInvoke, @NotNull Logger logger) {
        Intrinsics.checkNotNullParameter(show, "show");
        Intrinsics.checkNotNullParameter(adRepository, "adRepository");
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(getOperativeEventApi, "getOperativeEventApi");
        Intrinsics.checkNotNullParameter(getInitializationState, "getInitializationState");
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        Intrinsics.checkNotNullParameter(safeCallbackInvoke, "safeCallbackInvoke");
        Intrinsics.checkNotNullParameter(logger, "logger");
        this.show = show;
        this.adRepository = adRepository;
        this.sendDiagnosticEvent = sendDiagnosticEvent;
        this.getOperativeEventApi = getOperativeEventApi;
        this.getInitializationState = getInitializationState;
        this.sessionRepository = sessionRepository;
        this.safeCallbackInvoke = safeCallbackInvoke;
        this.logger = logger;
        this.hasStarted = StateFlowKt.MutableStateFlow(false);
        this.timeoutCancellationRequested = StateFlowKt.MutableStateFlow(false);
    }

    public static final /* synthetic */ MutableStateFlow access$getHasStarted$p(LegacyShowUseCase $this) {
        return $this.hasStarted;
    }

    public static final /* synthetic */ MutableStateFlow access$getTimeoutCancellationRequested$p(LegacyShowUseCase $this) {
        return $this.timeoutCancellationRequested;
    }

    public static final /* synthetic */ Object access$sendOperativeError(LegacyShowUseCase $this, OperativeEventRequestOuterClass$OperativeEventErrorType operativeEvent, String operativeMessage, AdObject adObject, Continuation $completion) {
        return $this.sendOperativeError(operativeEvent, operativeMessage, adObject, $completion);
    }

    public static final /* synthetic */ Show access$getShow$p(LegacyShowUseCase $this) {
        return $this.show;
    }

    public static final /* synthetic */ void access$setFullscreenAdShowing$cp(boolean z) {
        isFullscreenAdShowing = z;
    }

    public static final /* synthetic */ void access$showStarted(LegacyShowUseCase $this, TimeMark startTime, String placement, Listeners listeners) {
        $this.showStarted(startTime, placement, listeners);
    }

    public static final /* synthetic */ void access$showClicked(LegacyShowUseCase $this, TimeMark startTime, String placement, Listeners listeners) {
        $this.showClicked(startTime, placement, listeners);
    }

    public static final /* synthetic */ void access$showCompleted(LegacyShowUseCase $this, TimeMark startTime, String placement, ShowStatus status, Listeners listeners, String reason, String reasonDebug, UnityAdsShowOptions showOptions) {
        $this.showCompleted(startTime, placement, status, listeners, reason, reasonDebug, showOptions);
    }

    public static final /* synthetic */ void access$cancelTimeout(LegacyShowUseCase $this, TimeMark startTime) {
        $this.cancelTimeout(startTime);
    }

    public static final /* synthetic */ void access$bannerLeftApplication(LegacyShowUseCase $this, TimeMark startTime, String placement, Listeners listeners) {
        $this.bannerLeftApplication(startTime, placement, listeners);
    }

    public static final /* synthetic */ SessionRepository access$getSessionRepository$p(LegacyShowUseCase $this) {
        return $this.sessionRepository;
    }

    public static final /* synthetic */ Logger access$getLogger$p(LegacyShowUseCase $this) {
        return $this.logger;
    }

    public static final /* synthetic */ String access$getAdInfoString(LegacyShowUseCase $this) {
        return $this.getAdInfoString();
    }

    public static final /* synthetic */ AdObject access$getAdObject$p(LegacyShowUseCase $this) {
        return $this.adObject;
    }

    public static final /* synthetic */ AdObject access$getTmpAdObject(LegacyShowUseCase $this, String opportunityId) {
        return $this.getTmpAdObject(opportunityId);
    }

    public static final /* synthetic */ SendDiagnosticEvent access$getSendDiagnosticEvent$p(LegacyShowUseCase $this) {
        return $this.sendDiagnosticEvent;
    }

    public static final /* synthetic */ Map access$getTags(LegacyShowUseCase $this, String diagnosticReason, Integer code, String debugMessage, UnityAdsShowOptions showOptions) {
        return $this.getTags(diagnosticReason, code, debugMessage, showOptions);
    }

    public static final /* synthetic */ SafeCallbackInvoke access$getSafeCallbackInvoke$p(LegacyShowUseCase $this) {
        return $this.safeCallbackInvoke;
    }

    /* JADX WARN: Code duplicated, block: B:156:0x0531  */
    /* JADX WARN: Code duplicated, block: B:31:0x015f  */
    /* JADX WARN: Code duplicated, block: B:68:0x023c  */
    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v37 */
    /* JADX WARN: Type inference failed for: r26v0 */
    /* JADX WARN: Type inference failed for: r26v1 */
    /* JADX WARN: Type inference failed for: r26v6 */
    @Nullable
    public final Object invoke(@Nullable String str, @Nullable UnityAdsShowOptions unityAdsShowOptions, @NotNull Listeners listeners, @NotNull Continuation<? super Unit> continuation) {
        LegacyShowUseCase$invoke$1 legacyShowUseCase$invoke$1;
        ?? r26;
        ByteString byteString;
        Object obj;
        Object string;
        boolean z;
        String string2;
        String string3;
        if (continuation instanceof LegacyShowUseCase$invoke$1) {
            legacyShowUseCase$invoke$1 = (LegacyShowUseCase$invoke$1) continuation;
            if ((legacyShowUseCase$invoke$1.label & Integer.MIN_VALUE) != 0) {
                legacyShowUseCase$invoke$1.label -= Integer.MIN_VALUE;
            } else {
                legacyShowUseCase$invoke$1 = new LegacyShowUseCase$invoke$1(this, continuation);
            }
        } else {
            legacyShowUseCase$invoke$1 = new LegacyShowUseCase$invoke$1(this, continuation);
        }
        Object obj2 = legacyShowUseCase$invoke$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        switch (legacyShowUseCase$invoke$1.label) {
            case 0:
                ResultKt.throwOnFailure(obj2);
                long j = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
                this.placement = str;
                this.unityAdsShowOptions = unityAdsShowOptions;
                this.logger.debug("Show for placement " + str + " called");
                Ref$BooleanRef ref$BooleanRef = new Ref$BooleanRef();
                Ref$BooleanRef ref$BooleanRef2 = new Ref$BooleanRef();
                try {
                    Result$Companion result$Companion = Result.Companion;
                    obj = Result.constructor-impl(unityAdsShowOptions != null ? getOpportunityId(unityAdsShowOptions) : null);
                    break;
                } catch (Throwable th) {
                    Result$Companion result$Companion2 = Result.Companion;
                    obj = Result.constructor-impl(ResultKt.createFailure(th));
                }
                Object obj3 = obj;
                if (Result.exceptionOrNull-impl(obj3) == null) {
                    string = obj3;
                } else {
                    ref$BooleanRef.element = true;
                    string = UUID.randomUUID().toString();
                }
                String string4 = (String) string;
                if (string4 == null) {
                    LegacyShowUseCase legacyShowUseCase = this;
                    if (str != null) {
                        ByteString byteStringPollOpportunityIdForPlacement = legacyShowUseCase.adRepository.pollOpportunityIdForPlacement(str);
                        if (byteStringPollOpportunityIdForPlacement != null) {
                            UUID uuid = ProtobufExtensionsKt.toUUID(byteStringPollOpportunityIdForPlacement);
                            if (uuid != null) {
                                string3 = uuid.toString();
                            } else {
                                string3 = null;
                            }
                        } else {
                            string3 = null;
                        }
                        String str2 = string3;
                        if (str2 == null) {
                            ref$BooleanRef2.element = true;
                            string4 = UUID.randomUUID().toString();
                        } else {
                            string4 = str2;
                        }
                    } else {
                        string4 = UUID.randomUUID().toString();
                    }
                    Intrinsics.checkNotNullExpressionValue(string4, "if (placement != null) {….toString()\n            }");
                }
                String str3 = string4;
                showStart(str3, unityAdsShowOptions);
                TimeSource$Monotonic$ValueTimeMark timeSource$Monotonic$ValueTimeMark = TimeSource$Monotonic$ValueTimeMark.box-impl(j);
                String str4 = str;
                if (str4 == null) {
                    str4 = "";
                }
                Function6<String, UnityAds$UnityAdsShowError, String, Integer, String, Continuation<? super Unit>, Object> function6ShowError = showError(timeSource$Monotonic$ValueTimeMark, str4, str3, listeners, unityAdsShowOptions);
                if (GetInitializationState$DefaultImpls.invoke$default(this.getInitializationState, false, 1, null) != InitializationState.INITIALIZED) {
                    legacyShowUseCase$invoke$1.label = 1;
                    if (function6ShowError.invoke("not_initialized", UnityAds$UnityAdsShowError.NOT_INITIALIZED, LoadResult.MSG_NOT_INITIALIZED, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                if (str == null) {
                    legacyShowUseCase$invoke$1.label = 2;
                    if (function6ShowError.invoke("placement_null", UnityAds$UnityAdsShowError.INVALID_ARGUMENT, LoadResult.MSG_PLACEMENT_NULL, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                if (ref$BooleanRef.element) {
                    if (unityAdsShowOptions != null) {
                        JSONObject data = unityAdsShowOptions.getData();
                        if (data != null) {
                            Object objOpt = data.opt("objectId");
                            if (objOpt != null) {
                                string2 = objOpt.toString();
                            } else {
                                string2 = null;
                            }
                        } else {
                            string2 = null;
                        }
                    } else {
                        string2 = null;
                    }
                    UnityAds$UnityAdsShowError unityAds$UnityAdsShowError = UnityAds$UnityAdsShowError.INVALID_ARGUMENT;
                    legacyShowUseCase$invoke$1.label = 3;
                    if (function6ShowError.invoke("no_opportunity_id", unityAds$UnityAdsShowError, MESSAGE_OPPORTUNITY_ID, (Object) null, string2, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                if (ref$BooleanRef2.element) {
                    UnityAds$UnityAdsShowError unityAds$UnityAdsShowError2 = UnityAds$UnityAdsShowError.INVALID_ARGUMENT;
                    Object[] objArr = {str};
                    String str5 = String.format(MESSAGE_PLACEMENT_NOT_LOADED, Arrays.copyOf(objArr, objArr.length));
                    Intrinsics.checkNotNullExpressionValue(str5, "format(this, *args)");
                    legacyShowUseCase$invoke$1.label = 4;
                    if (function6ShowError.invoke("placement_not_loaded", unityAds$UnityAdsShowError2, str5, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                UUID uuidFromString = UUID.fromString(str3);
                Intrinsics.checkNotNullExpressionValue(uuidFromString, "fromString(opportunityId)");
                byteString = ProtobufExtensionsKt.toByteString(uuidFromString);
                AdObject ad = this.adRepository.getAd(byteString);
                this.adObject = ad;
                if (ad == null) {
                    legacyShowUseCase$invoke$1.label = 5;
                    if (function6ShowError.invoke("ad_object_not_found", UnityAds$UnityAdsShowError.INTERNAL_ERROR, MESSAGE_NO_AD_OBJECT + str3, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                if (ad.getState().getValue() == AdObjectState.EXPIRED) {
                    legacyShowUseCase$invoke$1.L$0 = this;
                    legacyShowUseCase$invoke$1.L$1 = byteString;
                    legacyShowUseCase$invoke$1.label = 6;
                    if (function6ShowError.invoke("ad_object_expired", UnityAds$UnityAdsShowError.EXPIRED, MESSAGE_AD_OBJECT_EXPIRED, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    this.adRepository.removeAd(byteString);
                    return Unit.INSTANCE;
                }
                AdPlayer adPlayer = ad.getAdPlayer();
                if (adPlayer != null) {
                    CoroutineScope scope = adPlayer.getScope();
                    z = (scope == null || CoroutineScopeKt.isActive(scope)) ? false : true;
                } else {
                    z = false;
                }
                if (z) {
                    legacyShowUseCase$invoke$1.label = 7;
                    if (function6ShowError.invoke("ad_player_scope_not_active", UnityAds$UnityAdsShowError.INTERNAL_ERROR, MESSAGE_AD_PLAYER_UNAVAILABLE, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                boolean z2 = ad.getAdPlayer() instanceof EmbeddableAdPlayer;
                if (!z2 && isFullscreenAdShowing) {
                    legacyShowUseCase$invoke$1.label = 8;
                    if (function6ShowError.invoke("already_showing", UnityAds$UnityAdsShowError.ALREADY_SHOWING, MESSAGE_ALREADY_SHOWING, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                if (this.sessionRepository.getNativeConfiguration().getFeatureFlags().getOpportunityIdPlacementValidation() && !Intrinsics.areEqual(ad.getPlacementId(), str)) {
                    legacyShowUseCase$invoke$1.label = 9;
                    if (function6ShowError.invoke("placement_validation", UnityAds$UnityAdsShowError.INVALID_ARGUMENT, MSG_OPPORTUNITY_AND_PLACEMENT_NOT_MATCHING, (Object) null, (Object) null, legacyShowUseCase$invoke$1) == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    return Unit.INSTANCE;
                }
                long showTimeoutMs = this.sessionRepository.getNativeConfiguration().getAdOperations().getShowTimeoutMs();
                if (!z2) {
                    LegacyShowUseCase$Companion legacyShowUseCase$Companion = Companion;
                    isFullscreenAdShowing = true;
                }
                Flow flowTimeoutAfter$default = FlowExtensionsKt.timeoutAfter$default(this.show.invoke(ad, unityAdsShowOptions), showTimeoutMs, false, new LegacyShowUseCase$invoke$2(this, ad, true, function6ShowError, str, null), 2, null);
                boolean z3 = z2;
                legacyShowUseCase$invoke$1.I$0 = z2 ? 1 : 0;
                legacyShowUseCase$invoke$1.label = 10;
                r26 = z2;
                if (FlowKt.catch(flowTimeoutAfter$default, new LegacyShowUseCase$invoke$3(function6ShowError, z3, null)).collect(new LegacyShowUseCase$invoke$4(this, j, str, listeners, unityAdsShowOptions, ad, function6ShowError), legacyShowUseCase$invoke$1) == coroutine_suspended) {
                    return coroutine_suspended;
                }
                if (r26 == 0) {
                    LegacyShowUseCase$Companion legacyShowUseCase$Companion2 = Companion;
                    isFullscreenAdShowing = false;
                }
                return Unit.INSTANCE;
            case 1:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 2:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 3:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 4:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 5:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 6:
                byteString = (ByteString) legacyShowUseCase$invoke$1.L$1;
                this = (LegacyShowUseCase) legacyShowUseCase$invoke$1.L$0;
                ResultKt.throwOnFailure(obj2);
                this.adRepository.removeAd(byteString);
                return Unit.INSTANCE;
            case 7:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 8:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 9:
                ResultKt.throwOnFailure(obj2);
                return Unit.INSTANCE;
            case 10:
                r26 = legacyShowUseCase$invoke$1.I$0;
                ResultKt.throwOnFailure(obj2);
                if (r26 == 0) {
                    LegacyShowUseCase$Companion legacyShowUseCase$Companion3 = Companion;
                    isFullscreenAdShowing = false;
                }
                return Unit.INSTANCE;
            default:
                throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
        }
    }

    public final void showReceivedReward(@NotNull TimeMark startTime, @NotNull String placement, @NotNull Listeners listeners) {
        Intrinsics.checkNotNullParameter(startTime, "startTime");
        Intrinsics.checkNotNullParameter(placement, "placement");
        Intrinsics.checkNotNullParameter(listeners, "listeners");
        this.logger.info("Rewarding ad " + getAdInfoString());
        this.hasStarted.setValue(true);
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_REWARDED, Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), (Map) null, (Map) null, this.adObject, (Integer) null, 44, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyShowUseCase$showReceivedReward$1(listeners, placement));
    }

    private final void bannerLeftApplication(TimeMark startTime, String placement, Listeners listeners) {
        this.logger.info("Left app while showing ad " + getAdInfoString());
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_LEFT_APP, Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), (Map) null, (Map) null, this.adObject, (Integer) null, 44, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyShowUseCase$bannerLeftApplication$1(listeners, placement));
    }

    private final Object sendOperativeError(OperativeEventRequestOuterClass$OperativeEventErrorType operativeEvent, String operativeMessage, AdObject adObject, Continuation<? super Unit> continuation) {
        OperativeEventErrorDataKt$Dsl$Companion operativeEventErrorDataKt$Dsl$Companion = OperativeEventErrorDataKt$Dsl.Companion;
        OperativeEventRequestOuterClass$OperativeEventErrorData$Builder operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder = OperativeEventRequestOuterClass$OperativeEventErrorData.newBuilder();
        Intrinsics.checkNotNullExpressionValue(operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder, "newBuilder()");
        OperativeEventErrorDataKt$Dsl $this$operativeEventErrorData_u24lambda_u240$iv = operativeEventErrorDataKt$Dsl$Companion._create(operativeEventRequestOuterClass$OperativeEventErrorData$BuilderNewBuilder);
        $this$operativeEventErrorData_u24lambda_u240$iv.setErrorType(operativeEvent);
        $this$operativeEventErrorData_u24lambda_u240$iv.setMessage(operativeMessage);
        OperativeEventRequestOuterClass$OperativeEventErrorData errorData = $this$operativeEventErrorData_u24lambda_u240$iv._build();
        GetOperativeEventApi getOperativeEventApi = this.getOperativeEventApi;
        OperativeEventRequestOuterClass$OperativeEventType operativeEventRequestOuterClass$OperativeEventType = OperativeEventRequestOuterClass$OperativeEventType.OPERATIVE_EVENT_TYPE_SHOW_ERROR;
        ByteString byteString = errorData.toByteString();
        Intrinsics.checkNotNullExpressionValue(byteString, "errorData.toByteString()");
        Object objInvoke = getOperativeEventApi.invoke(operativeEventRequestOuterClass$OperativeEventType, adObject, byteString, continuation);
        return objInvoke == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? objInvoke : Unit.INSTANCE;
    }

    private final void cancelTimeout(TimeMark startTime) {
        this.timeoutCancellationRequested.setValue(true);
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, "native_show_cancel_timeout", Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), (Map) null, (Map) null, this.adObject, (Integer) null, 44, (Object) null);
    }

    private final void showStarted(TimeMark startTime, String placement, Listeners listeners) {
        this.logger.info("Started showing ad " + getAdInfoString());
        this.hasStarted.setValue(true);
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_WV_STARTED, Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), (Map) null, (Map) null, this.adObject, (Integer) null, 44, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyShowUseCase$showStarted$1(listeners, placement));
    }

    private final void showClicked(TimeMark startTime, String placement, Listeners listeners) {
        this.logger.info("Clicked on ad " + getAdInfoString());
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_CLICKED, Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), (Map) null, (Map) null, this.adObject, (Integer) null, 44, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyShowUseCase$showClicked$1(listeners, placement));
    }

    private final String getOpportunityId(UnityAdsShowOptions unityAdsShowOptions) throws IllegalArgumentException {
        String it;
        JSONObject data = unityAdsShowOptions.getData();
        if (data != null) {
            Object objOpt = data.opt("objectId");
            if (objOpt != null && (it = objOpt.toString()) != null) {
                return UUID.fromString(it).toString();
            }
        }
        return null;
    }

    private final void showStart(String opportunityId, UnityAdsShowOptions showOptions) {
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_STARTED, (Double) null, MapsKt.mapOf(TuplesKt.to("new_api", String.valueOf((showOptions != null ? showOptions.showConfiguration : null) != null))), (Map) null, getTmpAdObject(opportunityId), (Integer) null, 42, (Object) null);
    }

    static /* synthetic */ void showCompleted$default(LegacyShowUseCase legacyShowUseCase, TimeMark timeMark, String str, ShowStatus showStatus, Listeners listeners, String str2, String str3, UnityAdsShowOptions unityAdsShowOptions, int i, Object obj) {
        if ((i & 16) != 0) {
            str2 = null;
        }
        if ((i & 32) != 0) {
            str3 = null;
        }
        legacyShowUseCase.showCompleted(timeMark, str, showStatus, listeners, str2, str3, unityAdsShowOptions);
    }

    private final void showCompleted(TimeMark startTime, String placement, ShowStatus status, Listeners listeners, String reason, String reasonDebug, UnityAdsShowOptions showOptions) {
        this.logger.info("Finished showing ad " + getAdInfoString());
        Map $this$showCompleted_u24lambda_u247 = MapsKt.createMapBuilder();
        if (reason != null) {
        }
        if (reasonDebug != null) {
        }
        TuplesKt.to("new_api", String.valueOf((showOptions != null ? showOptions.showConfiguration : null) != null));
        Map tags = MapsKt.build($this$showCompleted_u24lambda_u247);
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_SHOW_SUCCESS_TIME, Double.valueOf(TimeExtensionsKt.elapsedMillis(startTime)), tags, (Map) null, this.adObject, (Integer) null, 40, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyShowUseCase$showCompleted$1(listeners, placement, status, this));
    }

    private final Function6<String, UnityAds$UnityAdsShowError, String, Integer, String, Continuation<? super Unit>, Object> showError(TimeMark startTime, String placement, String opportunityId, Listeners listeners, UnityAdsShowOptions showOptions) {
        return new LegacyShowUseCase$showError$1(this, opportunityId, startTime, showOptions, listeners, placement, null);
    }

    private final Map<String, String> getTags(String diagnosticReason, Integer code, String debugMessage, UnityAdsShowOptions showOptions) {
        Pair[] pairArr = new Pair[3];
        pairArr[0] = TuplesKt.to("operation", OperationType.SHOW.toString());
        pairArr[1] = TuplesKt.to("reason", diagnosticReason);
        pairArr[2] = TuplesKt.to("new_api", String.valueOf((showOptions != null ? showOptions.showConfiguration : null) != null));
        Map<String, String> mapMutableMapOf = MapsKt.mutableMapOf(pairArr);
        if (code != null) {
            int it = code.intValue();
            mapMutableMapOf.put("reason_code", String.valueOf(it));
        }
        if (debugMessage != null) {
            mapMutableMapOf.put("reason_debug", debugMessage);
        }
        return mapMutableMapOf;
    }

    private final AdObject getTmpAdObject(String opportunityId) {
        UUID uuidFromString = UUID.fromString(opportunityId);
        Intrinsics.checkNotNullExpressionValue(uuidFromString, "fromString(opportunityId)");
        ByteString opportunityIdByteString = ProtobufExtensionsKt.toByteString(uuidFromString);
        AdObject adObject = this.adRepository.getAd(opportunityIdByteString);
        if (adObject != null) {
            return adObject;
        }
        SendDiagnosticEvent$Companion sendDiagnosticEvent$Companion = SendDiagnosticEvent.Companion;
        UUID uuidFromString2 = UUID.fromString(opportunityId);
        Intrinsics.checkNotNullExpressionValue(uuidFromString2, "fromString(opportunityId)");
        ByteString byteString = ProtobufExtensionsKt.toByteString(uuidFromString2);
        String str = this.placement;
        if (str == null) {
            str = "";
        }
        return SendDiagnosticEvent$Companion.getTmpAdObjectForEventSending$default(sendDiagnosticEvent$Companion, byteString, str, false, null, null, false, 60, null);
    }

    /* JADX WARN: Code duplicated, block: B:11:0x003b  */
    private final String getAdInfoString() {
        UUID uuid;
        StringBuilder sbAppend = new StringBuilder().append("for placement ");
        AdObject adObject = this.adObject;
        StringBuilder sbAppend2 = sbAppend.append(adObject != null ? adObject.getPlacementId() : null).append(" with instance id ");
        AdObject adObject2 = this.adObject;
        if (adObject2 != null) {
            ByteString opportunityId = adObject2.getOpportunityId();
            if (opportunityId != null) {
                uuid = ProtobufExtensionsKt.toUUID(opportunityId);
            } else {
                uuid = null;
            }
        } else {
            uuid = null;
        }
        return sbAppend2.append(uuid).toString();
    }
}