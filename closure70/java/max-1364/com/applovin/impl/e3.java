package com.applovin.impl;

import com.applovin.mediation.MaxAdFormat;
import java.util.Map;

/* JADX INFO: loaded from: classes.jar:com/applovin/impl/e3.class */
public class e3 {
    private final String a;
    private final MaxAdFormat b;
    private final Map c;
    private final Map d;
    private final Map e;
    private final h f;

    public e3(String str, MaxAdFormat maxAdFormat, Map map, Map map2, Map map3, h hVar) {
        this.a = str;
        this.b = maxAdFormat;
        this.c = map;
        this.d = map2;
        this.e = map3;
        this.f = hVar;
    }

    public String b() {
        return this.a;
    }

    public Map e() {
        return this.c;
    }

    public Map d() {
        return this.d;
    }

    public Map c() {
        return this.e;
    }

    public h f() {
        return this.f;
    }

    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof e3)) {
            return false;
        }
        e3 e3Var = (e3) obj;
        if (!e3Var.a(this)) {
            return false;
        }
        String strB = b();
        String strB2 = e3Var.b();
        if (strB == null) {
            if (strB2 != null) {
                return false;
            }
        } else if (!strB.equals(strB2)) {
            return false;
        }
        MaxAdFormat maxAdFormatA = a();
        MaxAdFormat maxAdFormatA2 = e3Var.a();
        if (maxAdFormatA == null) {
            if (maxAdFormatA2 != null) {
                return false;
            }
        } else if (!maxAdFormatA.equals(maxAdFormatA2)) {
            return false;
        }
        Map mapE = e();
        Map mapE2 = e3Var.e();
        if (mapE == null) {
            if (mapE2 != null) {
                return false;
            }
        } else if (!mapE.equals(mapE2)) {
            return false;
        }
        Map mapD = d();
        Map mapD2 = e3Var.d();
        if (mapD == null) {
            if (mapD2 != null) {
                return false;
            }
        } else if (!mapD.equals(mapD2)) {
            return false;
        }
        Map mapC = c();
        Map mapC2 = e3Var.c();
        if (mapC == null) {
            if (mapC2 != null) {
                return false;
            }
        } else if (!mapC.equals(mapC2)) {
            return false;
        }
        h hVarF = f();
        h hVarF2 = e3Var.f();
        if (hVarF == null) {
            return hVarF2 == null;
        }
        return hVarF.equals(hVarF2);
    }

    protected boolean a(Object obj) {
        return obj instanceof e3;
    }

    public int hashCode() {
        String strB = b();
        int iHashCode = strB == null ? 43 : strB.hashCode();
        MaxAdFormat maxAdFormatA = a();
        int i = (59 + iHashCode) * 59;
        int iHashCode2 = maxAdFormatA == null ? 43 : maxAdFormatA.hashCode();
        Map mapE = e();
        int i2 = (i + iHashCode2) * 59;
        int iHashCode3 = mapE == null ? 43 : mapE.hashCode();
        Map mapD = d();
        int i3 = (i2 + iHashCode3) * 59;
        int iHashCode4 = mapD == null ? 43 : mapD.hashCode();
        Map mapC = c();
        int i4 = (i3 + iHashCode4) * 59;
        int iHashCode5 = mapC == null ? 43 : mapC.hashCode();
        h hVarF = f();
        return ((i4 + iHashCode5) * 59) + (hVarF == null ? 43 : hVarF.hashCode());
    }

    public String toString() {
        return "MediatedAdRequestParameters(adUnitId=" + b() + ", adFormat=" + a() + ")";
    }

    public MaxAdFormat a() {
        return this.b;
    }
}