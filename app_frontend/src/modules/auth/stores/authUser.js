import AuthApi from "@/api/AuthApi";
import { defineStore } from "pinia";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";


export const useUserStore = defineStore("user", () => {
  const router = useRouter();
  const user = ref({});

  onMounted(async () => {
    try {
      const { data } = await AuthApi.autenticacion();
      user.value = data.data;

    } catch (error) {

      user.value = null;
    }
  });

  async function logout() {
    try {
      localStorage.removeItem("access_token");
      await AuthApi.logout();
      user.value = {};
      
    } catch (error) {
    }
  }

  const getUserName = computed(() => user.value?.full_name || "");

  return {
    user,
    getUserName,
    logout,
  };
});
