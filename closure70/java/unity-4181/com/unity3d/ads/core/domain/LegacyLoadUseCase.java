package com.unity3d.ads.core.domain;

import android.content.Context;
import com.google.protobuf.ByteString;
import com.unity3d.ads.UnityAdsErrorKt;
import com.unity3d.ads.UnityAdsLoadOptions;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.model.AdObjectState;
import com.unity3d.ads.core.data.model.Failure;
import com.unity3d.ads.core.data.model.LoadResult;
import com.unity3d.ads.core.data.model.OperationType;
import com.unity3d.ads.core.data.model.Success;
import com.unity3d.ads.core.data.repository.AdRepository;
import com.unity3d.ads.core.data.repository.SessionRepository;
import com.unity3d.ads.core.extensions.ExceptionExtensionsKt;
import com.unity3d.ads.core.extensions.ProtobufExtensionsKt;
import com.unity3d.ads.core.extensions.TimeExtensionsKt;
import com.unity3d.ads.core.log.Logger;
import com.unity3d.ads.core.log.Logger$DefaultImpls;
import com.unity3d.services.UnityAdsConstants$Messages;
import com.unity3d.services.banners.UnityBannerSize;
import gatewayprotocol.v1.AdRequestOuterClass$BannerSize;
import gatewayprotocol.v1.AdRequestOuterClass$BannerSize$Builder;
import gatewayprotocol.v1.BannerSizeKt$Dsl;
import gatewayprotocol.v1.BannerSizeKt$Dsl$Companion;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticAdType;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.ErrorOuterClass$PublicErrorCode;
import gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup;
import java.util.Map;
import java.util.UUID;
import kotlin.Metadata;
import kotlin.Pair;
import kotlin.ResultKt;
import kotlin.TuplesKt;
import kotlin.Unit;
import kotlin.collections.MapsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import kotlin.time.TimeMark;
import kotlin.time.TimeSource$Monotonic;
import kotlin.time.TimeSource$Monotonic$ValueTimeMark;
import kotlinx.coroutines.TimeoutKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.json.JSONObject;

/* JADX INFO: compiled from: LegacyLoadUseCase.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/LegacyLoadUseCase.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000¬\u0001\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010$\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0005\b\u0000\u0018\u0000 C2\u00020\u0001:\u0001CBM\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\t\u0012\u0006\u0010\n\u001a\u00020\u000b\u0012\u0006\u0010\f\u001a\u00020\r\u0012\u0006\u0010\u000e\u001a\u00020\u000f\u0012\u0006\u0010\u0010\u001a\u00020\u0011\u0012\u0006\u0010\u0012\u001a\u00020\u0013¢\u0006\u0002\u0010\u0014J\u0012\u0010#\u001a\u00020\u00162\b\u0010$\u001a\u0004\u0018\u00010\u0016H\u0002J\u0012\u0010%\u001a\u0004\u0018\u00010\u00162\u0006\u0010&\u001a\u00020\u001dH\u0002J\b\u0010'\u001a\u00020(H\u0002J\u0014\u0010)\u001a\u0004\u0018\u00010*2\b\u0010+\u001a\u0004\u0018\u00010,H\u0002J\u0014\u0010-\u001a\u0004\u0018\u00010.2\b\u0010\u0015\u001a\u0004\u0018\u00010\u0016H\u0002J\u0012\u0010/\u001a\u0004\u0018\u00010\u00162\u0006\u0010&\u001a\u00020\u001dH\u0002J,\u00100\u001a\u000e\u0012\u0004\u0012\u00020\u0016\u0012\u0004\u0012\u00020\u0016012\n\b\u0002\u00102\u001a\u0004\u0018\u00010\u00162\n\b\u0002\u00103\u001a\u0004\u0018\u00010\u0016H\u0002J\u001a\u00104\u001a\u0002052\u0006\u0010$\u001a\u00020\u00162\b\b\u0002\u00106\u001a\u00020\u0018H\u0002JA\u00107\u001a\u0002082\u0006\u00109\u001a\u00020:2\b\u0010 \u001a\u0004\u0018\u00010\u00162\u0006\u0010\u001c\u001a\u00020\u001d2\b\u0010;\u001a\u0004\u0018\u00010\u001b2\n\b\u0002\u0010+\u001a\u0004\u0018\u00010,H\u0086Bø\u0001\u0000¢\u0006\u0002\u0010<J\u0018\u0010=\u001a\u0002082\u0006\u0010$\u001a\u00020\u00162\u0006\u0010>\u001a\u00020?H\u0002J\u0010\u0010@\u001a\u00020\"2\u0006\u0010$\u001a\u00020\u0016H\u0002J\u0010\u0010A\u001a\u0002082\u0006\u0010B\u001a\u000205H\u0002R\u0010\u0010\u0015\u001a\u0004\u0018\u00010\u0016X\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\f\u001a\u00020\rX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0010\u001a\u00020\u0011X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0017\u001a\u00020\u0018X\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\u0019\u001a\u00020\u0018X\u0082\u000e¢\u0006\u0002\n\u0000R\u0010\u0010\u001a\u001a\u0004\u0018\u00010\u001bX\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u001c\u001a\u00020\u001dX\u0082.¢\u0006\u0002\n\u0000R\u000e\u0010\u0012\u001a\u00020\u0013X\u0082\u0004¢\u0006\u0002\n\u0000R\u0010\u0010\u001e\u001a\u0004\u0018\u00010\u001fX\u0082\u000e¢\u0006\u0002\n\u0000R\u0010\u0010 \u001a\u0004\u0018\u00010\u0016X\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000R\u0010\u0010!\u001a\u0004\u0018\u00010\"X\u0082\u000e¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006D"}, d2 = {"Lcom/unity3d/ads/core/domain/LegacyLoadUseCase;", "", "load", "Lcom/unity3d/ads/core/domain/Load;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "getInitializationState", "Lcom/unity3d/ads/core/domain/GetInitializationState;", "awaitInitialization", "Lcom/unity3d/ads/core/domain/AwaitInitialization;", "sessionRepository", "Lcom/unity3d/ads/core/data/repository/SessionRepository;", "adRepository", "Lcom/unity3d/ads/core/data/repository/AdRepository;", "safeCallbackInvoke", "Lcom/unity3d/ads/core/domain/SafeCallbackInvoke;", "cleanUpWhenOpportunityExpires", "Lcom/unity3d/ads/core/domain/CleanUpWhenOpportunityExpires;", "logger", "Lcom/unity3d/ads/core/log/Logger;", "(Lcom/unity3d/ads/core/domain/Load;Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;Lcom/unity3d/ads/core/domain/GetInitializationState;Lcom/unity3d/ads/core/domain/AwaitInitialization;Lcom/unity3d/ads/core/data/repository/SessionRepository;Lcom/unity3d/ads/core/data/repository/AdRepository;Lcom/unity3d/ads/core/domain/SafeCallbackInvoke;Lcom/unity3d/ads/core/domain/CleanUpWhenOpportunityExpires;Lcom/unity3d/ads/core/log/Logger;)V", LegacyLoadUseCase.KEY_AD_MARKUP, "", "isBanner", "", HandleInvocationsFromAdViewer.KEY_IS_HEADER_BIDDING, "listener", "Lcom/unity3d/ads/core/domain/InternalLoadListener;", HandleInvocationsFromAdViewer.KEY_LOAD_OPTIONS, "Lcom/unity3d/ads/UnityAdsLoadOptions;", "opportunity", "Lcom/google/protobuf/ByteString;", "placement", "startTime", "Lkotlin/time/TimeMark;", "getAdInfoString", "opportunityId", "getAdMarkup", "unityAdsLoadOptions", "getAdType", "Lgatewayprotocol/v1/DiagnosticEventRequestOuterClass$DiagnosticAdType;", "getBannerSize", "Lgatewayprotocol/v1/AdRequestOuterClass$BannerSize;", "bannerSize", "Lcom/unity3d/services/banners/UnityBannerSize;", "getHeaderBiddingAdMarkup", "Lgatewayprotocol/v1/HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup;", "getOpportunityId", "getTags", "", "reason", "reasonDebug", "getTmpAdObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "isScarAd", "invoke", "", "context", "Landroid/content/Context;", "unityLoadListener", "(Landroid/content/Context;Ljava/lang/String;Lcom/unity3d/ads/UnityAdsLoadOptions;Lcom/unity3d/ads/core/domain/InternalLoadListener;Lcom/unity3d/services/banners/UnityBannerSize;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "loadFailure", "loadResult", "Lcom/unity3d/ads/core/data/model/LoadResult$Failure;", "loadStart", "loadSuccess", "adObject", "Companion", "unity-ads_defaultRelease"})
@SourceDebugExtension({"SMAP\nLegacyLoadUseCase.kt\nKotlin\n*S Kotlin\n*F\n+ 1 LegacyLoadUseCase.kt\ncom/unity3d/ads/core/domain/LegacyLoadUseCase\n+ 2 BannerSizeKt.kt\ngatewayprotocol/v1/BannerSizeKtKt\n+ 3 fake.kt\nkotlin/jvm/internal/FakeKt\n*L\n1#1,295:1\n10#2:296\n1#3:297\n*S KotlinDebug\n*F\n+ 1 LegacyLoadUseCase.kt\ncom/unity3d/ads/core/domain/LegacyLoadUseCase\n*L\n199#1:296\n199#1:297\n*E\n"})
public final class LegacyLoadUseCase {

    @NotNull
    public static final LegacyLoadUseCase$Companion Companion = new LegacyLoadUseCase$Companion(null);

    @NotNull
    private final Load load;

    @NotNull
    private final SendDiagnosticEvent sendDiagnosticEvent;

    @NotNull
    private final GetInitializationState getInitializationState;

    @NotNull
    private final AwaitInitialization awaitInitialization;

    @NotNull
    private final SessionRepository sessionRepository;

    @NotNull
    private final AdRepository adRepository;

    @NotNull
    private final SafeCallbackInvoke safeCallbackInvoke;

    @NotNull
    private final CleanUpWhenOpportunityExpires cleanUpWhenOpportunityExpires;

    @NotNull
    private final Logger logger;
    private boolean isHeaderBidding;
    private boolean isBanner;

    @Nullable
    private InternalLoadListener listener;

    @Nullable
    private TimeMark startTime;

    @Nullable
    private String placement;

    @Nullable
    private ByteString opportunity;

    @Nullable
    private String adMarkup;
    private UnityAdsLoadOptions loadOptions;

    @NotNull
    public static final String KEY_OBJECT_ID = "objectId";

    @NotNull
    public static final String KEY_AD_MARKUP = "adMarkup";

    public LegacyLoadUseCase(@NotNull Load load, @NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull GetInitializationState getInitializationState, @NotNull AwaitInitialization awaitInitialization, @NotNull SessionRepository sessionRepository, @NotNull AdRepository adRepository, @NotNull SafeCallbackInvoke safeCallbackInvoke, @NotNull CleanUpWhenOpportunityExpires cleanUpWhenOpportunityExpires, @NotNull Logger logger) {
        Intrinsics.checkNotNullParameter(load, "load");
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(getInitializationState, "getInitializationState");
        Intrinsics.checkNotNullParameter(awaitInitialization, "awaitInitialization");
        Intrinsics.checkNotNullParameter(sessionRepository, "sessionRepository");
        Intrinsics.checkNotNullParameter(adRepository, "adRepository");
        Intrinsics.checkNotNullParameter(safeCallbackInvoke, "safeCallbackInvoke");
        Intrinsics.checkNotNullParameter(cleanUpWhenOpportunityExpires, "cleanUpWhenOpportunityExpires");
        Intrinsics.checkNotNullParameter(logger, "logger");
        this.load = load;
        this.sendDiagnosticEvent = sendDiagnosticEvent;
        this.getInitializationState = getInitializationState;
        this.awaitInitialization = awaitInitialization;
        this.sessionRepository = sessionRepository;
        this.adRepository = adRepository;
        this.safeCallbackInvoke = safeCallbackInvoke;
        this.cleanUpWhenOpportunityExpires = cleanUpWhenOpportunityExpires;
        this.logger = logger;
    }

    public static final /* synthetic */ void access$setOpportunity$p(LegacyLoadUseCase $this, ByteString byteString) {
        $this.opportunity = byteString;
    }

    public static final /* synthetic */ AdRepository access$getAdRepository$p(LegacyLoadUseCase $this) {
        return $this.adRepository;
    }

    public static final /* synthetic */ HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup access$getHeaderBiddingAdMarkup(LegacyLoadUseCase $this, String adMarkup) {
        return $this.getHeaderBiddingAdMarkup(adMarkup);
    }

    public static final /* synthetic */ String access$getAdMarkup$p(LegacyLoadUseCase $this) {
        return $this.adMarkup;
    }

    public static final /* synthetic */ GetInitializationState access$getGetInitializationState$p(LegacyLoadUseCase $this) {
        return $this.getInitializationState;
    }

    public static final /* synthetic */ Load access$getLoad$p(LegacyLoadUseCase $this) {
        return $this.load;
    }

    public static final /* synthetic */ SessionRepository access$getSessionRepository$p(LegacyLoadUseCase $this) {
        return $this.sessionRepository;
    }

    public static final /* synthetic */ AwaitInitialization access$getAwaitInitialization$p(LegacyLoadUseCase $this) {
        return $this.awaitInitialization;
    }

    public static final /* synthetic */ InternalLoadListener access$getListener$p(LegacyLoadUseCase $this) {
        return $this.listener;
    }

    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    /* JADX WARN: Not initialized variable reg: 19, insn: 0x01e0: MOVE (r1 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY]) = (r19 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY] A[D('opportunityId' java.lang.String)]), block:B:44:0x01b7 */
    @Nullable
    public final Object invoke(@NotNull Context context, @Nullable String placement, @NotNull UnityAdsLoadOptions loadOptions, @Nullable InternalLoadListener unityLoadListener, @Nullable UnityBannerSize bannerSize, @NotNull Continuation<? super Unit> continuation) {
        LegacyLoadUseCase$invoke$1 legacyLoadUseCase$invoke$1;
        String opportunityId;
        String opportunityId2;
        Object objWithTimeoutOrNull;
        if (continuation instanceof LegacyLoadUseCase$invoke$1) {
            legacyLoadUseCase$invoke$1 = (LegacyLoadUseCase$invoke$1) continuation;
            if ((legacyLoadUseCase$invoke$1.label & Integer.MIN_VALUE) != 0) {
                legacyLoadUseCase$invoke$1.label -= Integer.MIN_VALUE;
            } else {
                legacyLoadUseCase$invoke$1 = new LegacyLoadUseCase$invoke$1(this, continuation);
            }
        } else {
            legacyLoadUseCase$invoke$1 = new LegacyLoadUseCase$invoke$1(this, continuation);
        }
        Object $result = legacyLoadUseCase$invoke$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        try {
            switch (legacyLoadUseCase$invoke$1.label) {
                case 0:
                    ResultKt.throwOnFailure($result);
                    String opportunityId3 = getOpportunityId(loadOptions);
                    if (opportunityId3 == null) {
                        opportunityId3 = UUID.randomUUID().toString();
                        Intrinsics.checkNotNullExpressionValue(opportunityId3, "randomUUID().toString()");
                    }
                    opportunityId2 = opportunityId3;
                    this.logger.info("Load invoked for placement: " + placement + " with instance id: " + opportunityId2);
                    long timeoutMillis = this.sessionRepository.getNativeConfiguration().getAdOperations().getLoadTimeoutMs();
                    AdRequestOuterClass$BannerSize gatewayBannerSize = getBannerSize(bannerSize);
                    this.loadOptions = loadOptions;
                    this.adMarkup = getAdMarkup(loadOptions);
                    String str = this.adMarkup;
                    this.isHeaderBidding = !(str == null || StringsKt.isBlank(str));
                    this.isBanner = bannerSize != null;
                    this.listener = unityLoadListener;
                    this.placement = placement;
                    this.startTime = loadStart(opportunityId2);
                    legacyLoadUseCase$invoke$1.L$0 = this;
                    legacyLoadUseCase$invoke$1.L$1 = opportunityId2;
                    legacyLoadUseCase$invoke$1.label = 1;
                    objWithTimeoutOrNull = TimeoutKt.withTimeoutOrNull(timeoutMillis, new LegacyLoadUseCase$invoke$loadResult$1(opportunityId2, this, context, placement, gatewayBannerSize, loadOptions, null), legacyLoadUseCase$invoke$1);
                    if (objWithTimeoutOrNull == coroutine_suspended) {
                        return coroutine_suspended;
                    }
                    break;
                case 1:
                    opportunityId2 = (String) legacyLoadUseCase$invoke$1.L$1;
                    this = (LegacyLoadUseCase) legacyLoadUseCase$invoke$1.L$0;
                    ResultKt.throwOnFailure($result);
                    objWithTimeoutOrNull = $result;
                    break;
                default:
                    throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }
            Failure failure = (LoadResult) objWithTimeoutOrNull;
            if (failure == null) {
                failure = new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_TIMEOUT, UnityAdsErrorKt.MSG_BOLD_LOAD_FAIL_TIME_OUT, null, "timeout", null, false, 52, null);
            }
            LoadResult loadResult = failure;
            if (loadResult instanceof Success) {
                this.loadSuccess(((Success) loadResult).getAdObject());
            } else if (loadResult instanceof Failure) {
                this.loadFailure(opportunityId2, (Failure) loadResult);
            }
        } catch (Throwable e) {
            loadFailure(opportunityId, new Failure(ErrorOuterClass$PublicErrorCode.PUBLIC_ERROR_CODE_UNSPECIFIED, UnityAdsConstants$Messages.MSG_INTERNAL_ERROR, e, "uncaught_exception", ExceptionExtensionsKt.getShortenedStackTrace$default(e, 0, 1, null), false, 32, null));
        }
        return Unit.INSTANCE;
    }

    public static /* synthetic */ Object invoke$default(LegacyLoadUseCase legacyLoadUseCase, Context context, String str, UnityAdsLoadOptions unityAdsLoadOptions, InternalLoadListener internalLoadListener, UnityBannerSize unityBannerSize, Continuation continuation, int i, Object obj) {
        if ((i & 16) != 0) {
            unityBannerSize = null;
        }
        return legacyLoadUseCase.invoke(context, str, unityAdsLoadOptions, internalLoadListener, unityBannerSize, continuation);
    }

    /*  JADX ERROR: JadxRuntimeException in pass: BlockSplitter
        jadx.core.utils.exceptions.JadxRuntimeException: Unexpected missing predecessor for block: B:9:0x0018
        	at jadx.core.dex.visitors.blocks.BlockSplitter.addTempConnectionsForExcHandlers(BlockSplitter.java:280)
        	at jadx.core.dex.visitors.blocks.BlockSplitter.visit(BlockSplitter.java:79)
        */
    private final gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup getHeaderBiddingAdMarkup(java.lang.String r6) {
        /*
            r5 = this;
            r0 = r6
            java.lang.CharSequence r0 = (java.lang.CharSequence) r0
            r7 = r0
            r0 = r7
            if (r0 == 0) goto L10
            r0 = r7
            boolean r0 = kotlin.text.StringsKt.isBlank(r0)
            if (r0 == 0) goto L14
        L10:
            r0 = 1
            goto L15
        L14:
            r0 = 0
        L15:
            if (r0 != 0) goto L31
        L19:
            r0 = r6
            r1 = 0
            r2 = 1
            r3 = 0
            com.google.protobuf.ByteString r0 = com.unity3d.ads.core.extensions.ProtobufExtensionsKt.fromBase64$default(r0, r1, r2, r3)     // Catch: java.lang.Exception -> L2a
            byte[] r0 = r0.toByteArray()     // Catch: java.lang.Exception -> L2a
            gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup r0 = gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup.parseFrom(r0)     // Catch: java.lang.Exception -> L2a
            r7 = r0
            goto L2d
        L2a:
            r8 = move-exception
            r0 = 0
            return r0
        L2d:
            r0 = r7
            goto L34
        L31:
            gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup r0 = gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup.getDefaultInstance()
        L34:
            return r0
        */
        throw new UnsupportedOperationException("Method not decompiled: com.unity3d.ads.core.domain.LegacyLoadUseCase.getHeaderBiddingAdMarkup(java.lang.String):gatewayprotocol.v1.HeaderBiddingAdMarkupOuterClass$HeaderBiddingAdMarkup");
    }

    private final AdRequestOuterClass$BannerSize getBannerSize(UnityBannerSize bannerSize) {
        if (bannerSize == null) {
            return null;
        }
        BannerSizeKt$Dsl$Companion bannerSizeKt$Dsl$Companion = BannerSizeKt$Dsl.Companion;
        AdRequestOuterClass$BannerSize$Builder adRequestOuterClass$BannerSize$BuilderNewBuilder = AdRequestOuterClass$BannerSize.newBuilder();
        Intrinsics.checkNotNullExpressionValue(adRequestOuterClass$BannerSize$BuilderNewBuilder, "newBuilder()");
        BannerSizeKt$Dsl $this$bannerSize_u24lambda_u240$iv = bannerSizeKt$Dsl$Companion._create(adRequestOuterClass$BannerSize$BuilderNewBuilder);
        $this$bannerSize_u24lambda_u240$iv.setWidth(bannerSize.getWidth());
        $this$bannerSize_u24lambda_u240$iv.setHeight(bannerSize.getHeight());
        return $this$bannerSize_u24lambda_u240$iv._build();
    }

    private final String getOpportunityId(UnityAdsLoadOptions unityAdsLoadOptions) {
        JSONObject data = unityAdsLoadOptions.getData();
        if (data != null) {
            Object objOpt = data.opt("objectId");
            if (objOpt != null) {
                return objOpt.toString();
            }
        }
        return null;
    }

    private final String getAdMarkup(UnityAdsLoadOptions unityAdsLoadOptions) {
        JSONObject data = unityAdsLoadOptions.getData();
        if (data != null) {
            Object objOpt = data.opt(KEY_AD_MARKUP);
            if (objOpt != null) {
                return objOpt.toString();
            }
        }
        return null;
    }

    private final TimeMark loadStart(String opportunityId) {
        long startTime = TimeSource$Monotonic.INSTANCE.markNow-z9LOYto();
        SendDiagnosticEvent$DefaultImpls.invoke$default(this.sendDiagnosticEvent, DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_STARTED, (Double) null, getTags$default(this, null, null, 3, null), (Map) null, getTmpAdObject$default(this, opportunityId, false, 2, null), (Integer) null, 42, (Object) null);
        return TimeSource$Monotonic$ValueTimeMark.box-impl(startTime);
    }

    private final void loadSuccess(AdObject adObject) {
        this.logger.info("Successfully loaded ad " + getAdInfoString(ProtobufExtensionsKt.toUUID(adObject.getOpportunityId()).toString()));
        adObject.getState().setValue(AdObjectState.LOADED);
        this.cleanUpWhenOpportunityExpires.invoke(adObject);
        SendDiagnosticEvent sendDiagnosticEvent = this.sendDiagnosticEvent;
        DiagnosticEventRequestOuterClass$DiagnosticEventType diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_SUCCESS_TIME;
        TimeMark timeMark = this.startTime;
        SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent, diagnosticEventRequestOuterClass$DiagnosticEventType, timeMark != null ? Double.valueOf(TimeExtensionsKt.elapsedMillis(timeMark)) : null, getTags$default(this, null, null, 3, null), (Map) null, adObject, (Integer) null, 40, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyLoadUseCase$loadSuccess$1(this, adObject));
    }

    private final void loadFailure(String opportunityId, Failure loadResult) {
        Logger$DefaultImpls.error$default(this.logger, "Failed to load ad " + getAdInfoString(opportunityId) + ", error: " + loadResult.getError() + " :: " + loadResult.getMessage(), null, 2, null);
        SendDiagnosticEvent sendDiagnosticEvent = this.sendDiagnosticEvent;
        DiagnosticEventRequestOuterClass$DiagnosticEventType diagnosticEventRequestOuterClass$DiagnosticEventType = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_LOAD_FAILURE_TIME;
        TimeMark timeMark = this.startTime;
        SendDiagnosticEvent$DefaultImpls.invoke$default(sendDiagnosticEvent, diagnosticEventRequestOuterClass$DiagnosticEventType, timeMark != null ? Double.valueOf(TimeExtensionsKt.elapsedMillis(timeMark)) : null, getTags(loadResult.getReason(), loadResult.getReasonDebug()), (Map) null, getTmpAdObject(opportunityId, loadResult.isScarAd()), (Integer) null, 40, (Object) null);
        this.safeCallbackInvoke.invoke(new LegacyLoadUseCase$loadFailure$1(this, loadResult));
    }

    static /* synthetic */ Map getTags$default(LegacyLoadUseCase legacyLoadUseCase, String str, String str2, int i, Object obj) {
        if ((i & 1) != 0) {
            str = null;
        }
        if ((i & 2) != 0) {
            str2 = null;
        }
        return legacyLoadUseCase.getTags(str, str2);
    }

    private final Map<String, String> getTags(String reason, String reasonDebug) {
        Pair[] pairArr = new Pair[3];
        pairArr[0] = TuplesKt.to("state", GetInitializationState$DefaultImpls.invoke$default(this.getInitializationState, false, 1, null).toString());
        pairArr[1] = TuplesKt.to("operation", OperationType.LOAD.toString());
        UnityAdsLoadOptions unityAdsLoadOptions = this.loadOptions;
        if (unityAdsLoadOptions == null) {
            Intrinsics.throwUninitializedPropertyAccessException(HandleInvocationsFromAdViewer.KEY_LOAD_OPTIONS);
            unityAdsLoadOptions = null;
        }
        pairArr[2] = TuplesKt.to("new_api", String.valueOf(unityAdsLoadOptions.loadConfiguration != null));
        Map<String, String> mapMutableMapOf = MapsKt.mutableMapOf(pairArr);
        String str = reason;
        if (!(str == null || str.length() == 0)) {
            mapMutableMapOf.put("reason", reason);
        }
        String str2 = reasonDebug;
        if (!(str2 == null || str2.length() == 0)) {
            mapMutableMapOf.put("reason_debug", reasonDebug);
        }
        return mapMutableMapOf;
    }

    private final DiagnosticEventRequestOuterClass$DiagnosticAdType getAdType() {
        return this.isBanner ? DiagnosticEventRequestOuterClass$DiagnosticAdType.DIAGNOSTIC_AD_TYPE_BANNER : DiagnosticEventRequestOuterClass$DiagnosticAdType.DIAGNOSTIC_AD_TYPE_FULLSCREEN;
    }

    static /* synthetic */ AdObject getTmpAdObject$default(LegacyLoadUseCase legacyLoadUseCase, String str, boolean z, int i, Object obj) {
        if ((i & 2) != 0) {
            z = false;
        }
        return legacyLoadUseCase.getTmpAdObject(str, z);
    }

    private final AdObject getTmpAdObject(String opportunityId, boolean isScarAd) {
        SendDiagnosticEvent$Companion sendDiagnosticEvent$Companion = SendDiagnosticEvent.Companion;
        UUID uuidFromString = UUID.fromString(opportunityId);
        Intrinsics.checkNotNullExpressionValue(uuidFromString, "fromString(opportunityId)");
        ByteString byteString = ProtobufExtensionsKt.toByteString(uuidFromString);
        String str = this.placement;
        UnityAdsLoadOptions unityAdsLoadOptions = this.loadOptions;
        if (unityAdsLoadOptions == null) {
            Intrinsics.throwUninitializedPropertyAccessException(HandleInvocationsFromAdViewer.KEY_LOAD_OPTIONS);
            unityAdsLoadOptions = null;
        }
        return sendDiagnosticEvent$Companion.getTmpAdObjectForEventSending(byteString, str, this.isHeaderBidding, unityAdsLoadOptions, getAdType(), isScarAd);
    }

    private final String getAdInfoString(String opportunityId) {
        return "for placement " + this.placement + " with instance id " + opportunityId;
    }
}