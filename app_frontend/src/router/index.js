
import { createRouter, createWebHistory } from "vue-router";

import AuthApi from "@/api/AuthApi";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/aside",
      name: "aside",
      meta: { requireAuth: true },
      component: () => import("@/components/AsideComponent.vue"),
    },

    {
      path: "/auth",
      name: "auth",
      component: () => import("@/modules/auth/layouts/AuthLayout.vue"),
      children: [
        {
          path: "registro",
          name: "registro",
          component: () => import("@/modules/auth/views/RegistroView.vue"),
        },
        {
          path: "login",
          name: "login",
          component: () => import("@/modules/auth/views/LoginView.vue"),
        },
        {
          path: "verificar-cuenta",
          name: "verificar-cuenta",
          component: () =>
            import("@/modules/auth/views/ConfirmarCuentaView.vue"),
        },
        {
          path: "olvide-password",
          name: "olvide-password",
          component: () =>
            import("@/modules/auth/views/OlvidePasswordView.vue"),
        },
        {
          path: "/password-reset-confirm/:uidb64/:token",
          name: "olvide-password-confirm",
          component: () =>
            import("@/modules/auth/views/NuevaContrasenaView.vue"),
        },
        {
          path: "nuevo-password",
          name: "nuevo-password",
          component: () =>
            import("@/modules/auth/views/NuevaContrasenaView.vue"),
        },

      ],
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const requireAuth = to.matched.some((url) => url.meta.requireAuth);

  const token = localStorage.getItem("access_token");

  if (requireAuth && !token) {
    next({ name: "login" });
  } else if (requireAuth && token) {
    try {
      await AuthApi.autenticacion();
      next();
    } catch (error) {
      localStorage.removeItem("access_token");
      next({ name: "login" });
    }
  }
  next();
});

export default router;
