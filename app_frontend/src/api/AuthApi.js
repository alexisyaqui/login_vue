import AuthApi from "@/lib/axios";

// Interceptor para agregar el token en cada solicitud
AuthApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default {
  registro(data) {
    return AuthApi.post("/usuario/registro/", data);
  },

  verificarCuenta(data) {
    return AuthApi.post("/usuario/verificar/", data);
  },

  login(data) {
    return AuthApi.post("/usuario/login/", data);
  },

  autenticacion() {
    return AuthApi.get("/usuario/autenticated/");
  },

  logout() {
    return AuthApi.post("/usuario/logout/", );
    
  },

  password_reset(data) {
    return AuthApi.post("/usuario/password-reset-confirm/", data);
  },

  password_reset_confirm(uidb64, token) {
    return AuthApi.get(`/usuario/password-reset-confirm/${uidb64}/${token}`);
  },

  nueva_contrasena(uidb64, token, { password, confirm_password }){
    return AuthApi.patch('/usuario/set-new-password/',  { uidb64, token, password, confirm_password });

  }
};
