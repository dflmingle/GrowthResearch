package com.unity3d.ads.core.domain.events;

import com.google.protobuf.ByteString;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.repository.OperativeEventRepository;
import com.unity3d.ads.core.domain.HandleInvocationsFromAdViewer;
import gatewayprotocol.v1.AdFormatOuterClass$AdFormat;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticAdType;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventRequest;
import gatewayprotocol.v1.OperativeEventRequestOuterClass$OperativeEventType;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/* JADX INFO: compiled from: GetOperativeEventApi.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/events/GetOperativeEventApi.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000B\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0000\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006JI\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\r\u001a\u00020\f2\u0006\u0010\u000e\u001a\u00020\f2\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00102\n\b\u0002\u0010\u0011\u001a\u0004\u0018\u00010\u0012H\u0086Bø\u0001\u0000¢\u0006\u0002\u0010\u0013J)\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u0014\u001a\u00020\u00152\u0006\u0010\u000e\u001a\u00020\fH\u0086Bø\u0001\u0000¢\u0006\u0002\u0010\u0016R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006\u0017"}, d2 = {"Lcom/unity3d/ads/core/domain/events/GetOperativeEventApi;", "", "operativeEventRepository", "Lcom/unity3d/ads/core/data/repository/OperativeEventRepository;", "operativeEventRequest", "Lcom/unity3d/ads/core/domain/events/GetOperativeEventRequest;", "(Lcom/unity3d/ads/core/data/repository/OperativeEventRepository;Lcom/unity3d/ads/core/domain/events/GetOperativeEventRequest;)V", "invoke", "", "operativeEventType", "Lgatewayprotocol/v1/OperativeEventRequestOuterClass$OperativeEventType;", "opportunityId", "Lcom/google/protobuf/ByteString;", HandleInvocationsFromAdViewer.KEY_TRACKING_TOKEN, "additionalEventData", "playerServerId", "", "adFormat", "Lgatewayprotocol/v1/AdFormatOuterClass$AdFormat;", "(Lgatewayprotocol/v1/OperativeEventRequestOuterClass$OperativeEventType;Lcom/google/protobuf/ByteString;Lcom/google/protobuf/ByteString;Lcom/google/protobuf/ByteString;Ljava/lang/String;Lgatewayprotocol/v1/AdFormatOuterClass$AdFormat;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "adObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "(Lgatewayprotocol/v1/OperativeEventRequestOuterClass$OperativeEventType;Lcom/unity3d/ads/core/data/model/AdObject;Lcom/google/protobuf/ByteString;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "unity-ads_defaultRelease"})
@SourceDebugExtension({"SMAP\nGetOperativeEventApi.kt\nKotlin\n*S Kotlin\n*F\n+ 1 GetOperativeEventApi.kt\ncom/unity3d/ads/core/domain/events/GetOperativeEventApi\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n*L\n1#1,48:1\n1#2:49\n*E\n"})
public final class GetOperativeEventApi {

    @NotNull
    private final OperativeEventRepository operativeEventRepository;

    @NotNull
    private final GetOperativeEventRequest operativeEventRequest;

    public GetOperativeEventApi(@NotNull OperativeEventRepository operativeEventRepository, @NotNull GetOperativeEventRequest operativeEventRequest) {
        Intrinsics.checkNotNullParameter(operativeEventRepository, "operativeEventRepository");
        Intrinsics.checkNotNullParameter(operativeEventRequest, "operativeEventRequest");
        this.operativeEventRepository = operativeEventRepository;
        this.operativeEventRequest = operativeEventRequest;
    }

    /* JADX WARN: Code duplicated, block: B:7:0x0029  */
    @Nullable
    public final Object invoke(@NotNull OperativeEventRequestOuterClass$OperativeEventType operativeEventType, @NotNull ByteString opportunityId, @NotNull ByteString trackingToken, @NotNull ByteString additionalEventData, @Nullable String playerServerId, @Nullable AdFormatOuterClass$AdFormat adFormat, @NotNull Continuation<? super Unit> continuation) {
        GetOperativeEventApi$invoke$1 getOperativeEventApi$invoke$1;
        Object objInvoke;
        if (continuation instanceof GetOperativeEventApi$invoke$1) {
            getOperativeEventApi$invoke$1 = (GetOperativeEventApi$invoke$1) continuation;
            if ((getOperativeEventApi$invoke$1.label & Integer.MIN_VALUE) != 0) {
                getOperativeEventApi$invoke$1.label -= Integer.MIN_VALUE;
            } else {
                getOperativeEventApi$invoke$1 = new GetOperativeEventApi$invoke$1(this, continuation);
            }
        } else {
            getOperativeEventApi$invoke$1 = new GetOperativeEventApi$invoke$1(this, continuation);
        }
        Object $result = getOperativeEventApi$invoke$1.result;
        Object coroutine_suspended = IntrinsicsKt.getCOROUTINE_SUSPENDED();
        switch (getOperativeEventApi$invoke$1.label) {
            case 0:
                ResultKt.throwOnFailure($result);
                getOperativeEventApi$invoke$1.L$0 = this;
                getOperativeEventApi$invoke$1.label = 1;
                objInvoke = this.operativeEventRequest.invoke(operativeEventType, trackingToken, opportunityId, additionalEventData, playerServerId, adFormat, getOperativeEventApi$invoke$1);
                if (objInvoke == coroutine_suspended) {
                    return coroutine_suspended;
                }
                break;
            case 1:
                this = (GetOperativeEventApi) getOperativeEventApi$invoke$1.L$0;
                ResultKt.throwOnFailure($result);
                objInvoke = $result;
                break;
            default:
                throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
        }
        OperativeEventRequestOuterClass$OperativeEventRequest operativeEvent = (OperativeEventRequestOuterClass$OperativeEventRequest) objInvoke;
        this.operativeEventRepository.addOperativeEvent(operativeEvent);
        return Unit.INSTANCE;
    }

    public static /* synthetic */ Object invoke$default(GetOperativeEventApi getOperativeEventApi, OperativeEventRequestOuterClass$OperativeEventType operativeEventRequestOuterClass$OperativeEventType, ByteString byteString, ByteString byteString2, ByteString byteString3, String str, AdFormatOuterClass$AdFormat adFormatOuterClass$AdFormat, Continuation continuation, int i, Object obj) {
        if ((i & 16) != 0) {
            str = null;
        }
        if ((i & 32) != 0) {
            adFormatOuterClass$AdFormat = null;
        }
        return getOperativeEventApi.invoke(operativeEventRequestOuterClass$OperativeEventType, byteString, byteString2, byteString3, str, adFormatOuterClass$AdFormat, continuation);
    }

    @Nullable
    public final Object invoke(@NotNull OperativeEventRequestOuterClass$OperativeEventType operativeEventType, @NotNull AdObject adObject, @NotNull ByteString additionalEventData, @NotNull Continuation<? super Unit> continuation) {
        AdFormatOuterClass$AdFormat adFormatOuterClass$AdFormat;
        ByteString opportunityId = adObject.getOpportunityId();
        ByteString trackingToken = adObject.getTrackingToken();
        GetOperativeEventApi getOperativeEventApi = this;
        OperativeEventRequestOuterClass$OperativeEventType operativeEventRequestOuterClass$OperativeEventType = operativeEventType;
        ByteString byteString = opportunityId;
        ByteString byteString2 = trackingToken;
        ByteString byteString3 = additionalEventData;
        String playerServerId = adObject.getPlayerServerId();
        if ((adObject.getAdType() == DiagnosticEventRequestOuterClass$DiagnosticAdType.DIAGNOSTIC_AD_TYPE_BANNER ? this : null) != null) {
            getOperativeEventApi = getOperativeEventApi;
            operativeEventRequestOuterClass$OperativeEventType = operativeEventRequestOuterClass$OperativeEventType;
            byteString = byteString;
            byteString2 = byteString2;
            byteString3 = byteString3;
            playerServerId = playerServerId;
            adFormatOuterClass$AdFormat = AdFormatOuterClass$AdFormat.AD_FORMAT_BANNER;
        } else {
            adFormatOuterClass$AdFormat = null;
        }
        Object objInvoke = getOperativeEventApi.invoke(operativeEventRequestOuterClass$OperativeEventType, byteString, byteString2, byteString3, playerServerId, adFormatOuterClass$AdFormat, continuation);
        return objInvoke == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? objInvoke : Unit.INSTANCE;
    }
}