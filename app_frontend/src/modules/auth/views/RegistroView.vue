<template>
    <div class="flex flex-col h-screen bg-gray-100">
        <!-- Auth Card Container -->
        <div class="grid place-items-center mx-1 my-10 sm:my-auto">

            <!-- Auth Card -->
            <div class="w-11/12 p-12 sm:w-8/12 md:w-6/12 lg:w-5/12 2xl:w-4/12 px-6 py-10 sm:px-10 sm:py-6 bg-white rounded-lg shadow-md lg:shadow-lg">

                <!-- Card Title -->
                <h2 class="text-center py-5 font-bold text-2xl lg:text-3xl text-indigo-800  uppercase">
                    Registrar Cuenta
                </h2>

                <FormKit 
                id="registerForm" 
                type="form" 
                :actions="false" 
                incomplete-messages="No se pudo enviar, revisa los datos"
                @submit="onRegistrar">

                    <FormKit type="email" label="Corroe Electronico" name="email"
                        placeholder="Ingrese su correo electronico" validation="required|email" :validation-messages="{
                            required: 'El correo electronico es obligatorio',
                            email: 'El nombre es muy corto'
                        }" />

                    <FormKit type="text" label="Primer Nombre" name="primer_nombre"
                        placeholder="Ingrese su primer nombre" validation="required|length:3" :validation-messages="{
                            required: 'El nombre es obligatorio',
                            length: 'El nombre es muy corto'
                        }" />

                    <FormKit type="text" label="Primer apellido" name="primer_apellido"
                        placeholder="Ingrese su primer apellido" validation="required|length:3" :validation-messages="{
                            required: 'El nombre es obligatorio',
                            length: 'El nombre es muy corto'
                        }" />

                    <FormKit type="password" label="Contraseña" name="password"
                        placeholder="Ingrese su Contraseña - Min 8 caracteres" validation="required|length:8"
                        :validation-messages="{
                            required: 'La contraseña es obligatorio',
                            length: 'La contraseña debe tener al meno 8 caracteres'
                        }" />

                    <FormKit type="password" label="Confirmar Contraseña" name="password2"
                        placeholder="Repite su contraseña" validation="required|confirm:password" :validation-messages="{
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
</template>



<script setup>
import AuthApi from '@/api/AuthApi';
import { toast } from 'vue3-toastify';
import {reset} from '@formkit/vue'
import { useRoute, useRouter } from 'vue-router';



const router = useRouter();


const onRegistrar = async (formData) => {
    try {
        const { data } = await AuthApi.registro(formData);

        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        setTimeout(() => {
            router.push({name: 'verificar-cuenta'})
        }, 5000);
        reset('registerForm')
    } catch (error) {
        console.log(error.response.data.error);

        toast(error.response.data.email, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
    }

}
</script>
