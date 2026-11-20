package com.applovin.impl.sdk;

import com.applovin.impl.c3;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/* JADX INFO: loaded from: classes.jar:com/applovin/impl/sdk/q.class */
public class q {
    private final p a;
    private final Map b = new HashMap(5);
    private final Object c = new Object();
    private final Map d = Collections.synchronizedMap(new HashMap(5));
    private final Map e = Collections.synchronizedMap(new HashMap(5));

    q(l lVar) {
        this.a = lVar.Q();
    }

    /* JADX WARN: Type inference failed for: r0v1, types: [java.lang.Object, java.lang.Throwable] */
    public void c(c3 c3Var) {
        ?? r0 = this.c;
        synchronized (r0) {
            try {
                if (p.a()) {
                    this.a.a("MediationWaterfallWinnerTracker", "Tracking winning ad: " + c3Var);
                }
                this.b.put(c3Var.getAdUnitId(), new q$a(c3Var.C(), c3Var.c(), c3Var.getNetworkName()));
            } catch (Throwable unused) {
                throw r0;
            }
        }
        this.e.put(c3Var.getAdUnitId(), c3Var.T());
    }

    public void b(c3 c3Var) {
        this.d.put(c3Var.getAdUnitId(), c3Var.T());
    }

    public String a(String str) {
        return (String) this.e.get(str);
    }

    public String b(String str) {
        return (String) this.d.get(str);
    }

    /* JADX WARN: Multi-variable type inference failed */
    public void a(c3 c3Var) {
        synchronized (this.c) {
            try {
                String adUnitId = c3Var.getAdUnitId();
                q$a q_a = (q$a) this.b.get(adUnitId);
                if (q_a == null) {
                    if (p.a()) {
                        this.a.a("MediationWaterfallWinnerTracker", "No previous winner to clear.");
                    }
                    return;
                }
                if (c3Var.C().equals(q_a.b())) {
                    if (p.a()) {
                        this.a.a("MediationWaterfallWinnerTracker", "Clearing previous winning ad: " + q_a);
                    }
                    this.b.remove(adUnitId);
                } else if (p.a()) {
                    this.a.a("MediationWaterfallWinnerTracker", "Previous winner not cleared for ad: " + c3Var + " , since it could have already been updated with a new ad: " + q_a);
                }
            } catch (Throwable unused) {
                throw this;
            }
        }
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v0, types: [com.applovin.impl.sdk.q] */
    /* JADX WARN: Type inference failed for: r0v1, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v4, types: [com.applovin.impl.sdk.q$a] */
    public q$a c(String str) {
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = (q$a) r0.b.get(str);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }
}