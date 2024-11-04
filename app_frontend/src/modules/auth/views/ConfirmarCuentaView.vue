<template>
    <div class="flex flex-col h-screen bg-gray-100">
        <!-- Auth Card Container -->
        <div class="grid place-items-center mx-1 my-10 sm:my-auto">

            <!-- Auth Card -->
            <div class="w-11/12 p-12 sm:w-8/12 md:w-6/12 lg:w-5/12 2xl:w-4/12 
            px-6 py-10 sm:px-10 sm:py-6 
            bg-white rounded-lg shadow-md lg:shadow-lg">

                <!-- Card Title -->
                <h2 class="text-center py-5 font-bold text-2xl lg:text-3xl text-indigo-800  uppercase">
                    VERIFICAR CUENTA DE USUARIO
                </h2>

                <FormKit 
                id="verificarCuentaForm" 
                type="form" 
                :actions="false"
                incomplete-messages="No se pudo enviar, revisa los datos"
                @submit="onVerificarCuenta">

                    <FormKit 
                    type="number" 
                    label="Ingrese el codigo OTP" 
                    name="otp"
                    placeholder="Ingrese el codigo de 6 digitos que recibio en su EMAIL"
                    validation="required|otp" 
                    :validation-messages="{
                    required: 'El codigo otp, es obligatorio',
                    otp: 'El nombre es muy corto'
                        }" />

                    <FormKit type="submit">Verificar Usuario</FormKit>

                </FormKit>

                <div class="sm:flex sm:flex-wrap mt-8 sm:mb-4 text-sm text-center">
                    <RouterLink to="login" class="flex-2 underline">
                        si ya tienes una cuenta Inicia sesion aqui
                    </RouterLink>


                </div>

            </div>
        </div>
    </div>
</template>



<script setup>
import AuthApi from '@/api/AuthApi';
import { toast } from 'vue3-toastify';
import { reset } from '@formkit/vue'
import { useRoute, useRouter } from 'vue-router';


const route = useRoute();
const router = useRouter();


const onVerificarCuenta = async (formData) => {
    try {
        const { data } = await AuthApi.verificarCuenta(formData);
        console.log(data);

        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        setTimeout(() => {
            router.push({name: 'login'})
        }, 3000);
        reset('verificarCuentaForm')
    } catch (error) {
        console.log(error.response.data.error);

        toast(error.response.data.message || error.response.data.otp, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        reset('verificarCuentaForm')
    }

}
</script>
