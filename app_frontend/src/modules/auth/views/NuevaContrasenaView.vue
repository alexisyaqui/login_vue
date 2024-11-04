<template>
<div v-if="validToken">
    <div class="flex flex-col h-screen bg-gray-100">
        <!-- Auth Card Container -->
        <div class="grid place-items-center mx-1 my-10 sm:my-auto">

            <!-- Auth Card -->
            <div class="w-11/12 p-12 sm:w-8/12 md:w-6/12 lg:w-5/12 2xl:w-4/12 
            px-6 py-10 sm:px-10 sm:py-6 
            bg-white rounded-lg shadow-md lg:shadow-lg">

                <!-- Card Title -->
                <h2 class="text-center py-5 font-bold text-2xl lg:text-3xl text-indigo-800  uppercase">
                    NUEVA CONTRASEÑA
                </h2>

                <FormKit 
                id="registerForm" 
                type="form"
                :actions="false" 
                incomplete-messages="No se pudo enviar, revisa los datos"
                @submit="onNuevaContrasena"
                >


                    <FormKit type="password" 
                    label="Contraseña" 
                    name="password"
                    placeholder="Ingrese su Contraseña - Min 8 caracteres" 
                    validation="required|length:8"
                    :validation-messages="{
                    required: 'La contraseña es obligatorio',
                    length: 'La contraseña debe tener al meno 8 caracteres'
                    }" />

                    <FormKit 
                    type="password" 
                    label="Confirmar Contraseña" 
                    name="confirm_password"
                    placeholder="Repite su contraseña" 
                    validation="required|confirm:password" 
                    :validation-messages="{
                    required: 'La contraseña es obligatorio',
                    confirm: 'La contraseña no son iguales'
                    }" />

                    <FormKit type="submit">Crear Cuenta</FormKit>



                </FormKit>
                <div class="sm:flex sm:flex-wrap mt-8 sm:mb-4 text-sm text-center">
                    <RouterLink to="login" class="flex-2 underline">
                        si ya tienes una cuenta Inicia sesion aqui
                    </RouterLink>


                </div>

            </div>
        </div>
    </div>
</div>
</template>



<script setup>
import AuthApi from '@/api/AuthApi';
import { toast } from 'vue3-toastify';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const route = useRoute();
const router = useRouter();
const { uidb64} = route.params;
const { token } = route.params;


const validToken = ref(false);

onMounted(async () => {

    try {
        const { data } = await AuthApi.password_reset_confirm(uidb64, token);

        validToken.value = true

        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
    } catch (error) {

        toast(error.message, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
    }
})


const onNuevaContrasena = async({password, confirm_password}) => {
    try {
        const { data } = await AuthApi.nueva_contrasena(uidb64, token, {password, confirm_password});
        
        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        setTimeout(() => {
            router.push({name: 'login'})
        }, 3000);

    } catch (error) {
        toast(error.response.data.message, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        
    }

}

</script>
