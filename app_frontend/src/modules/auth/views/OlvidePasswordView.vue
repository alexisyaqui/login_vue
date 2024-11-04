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
                    Restablecimiento de contraseña
                </h2>

                <FormKit 
                id="olvidePasswordForm" 
                type="form" 
                :actions="false"
                incomplete-messages="No se pudo enviar, revisa los datos" 
                @submit="onOlvidePassword">

                    <FormKit 
                    type="email" 
                    label="Correo Electronico" 
                    name="email"
                    placeholder="Ingrese su correo electronico con la que te hayas registrado "
                    validation="required|email" 
                    :validation-messages="{
                        required: 'El email, es obligatorio',
                        email: 'Email no valido'
                    }" />

                    <FormKit type="submit">Restablecer Contraseña</FormKit>

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



const onOlvidePassword = async ({email}) => {
    try {
        const { data } = await AuthApi.password_reset({email});
        console.log(data);

        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        reset('olvidePasswordForm')
    } catch (error) {
        console.log(error.response.data.message);

        toast(error.response.data.message, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
    }

}
</script>
