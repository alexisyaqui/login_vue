<template>
    <div class="flex flex-col h-screen bg-gray-100">
        <!-- Auth Card Container -->
        <div class="grid place-items-center mx-2 my-20 sm:my-auto">
            <div class="flex">
                <span class="text-center font-bold my-20 mx-auto">
                    <a href="https://egoistdeveloper.github.io/twcss-to-sass-playground/" target="_blank"
                        class="text-blue-600">
                        Convetert to SASS
                    </a>
                </span>
            </div>

            <!-- Auth Card -->
            <div
                class="w-11/12 p-12 sm:w-8/12 md:w-6/12 lg:w-5/12 2xl:w-4/12 px-6 py-5 sm:px-10 sm:py-6 bg-white rounded-lg shadow-md lg:shadow-lg">

                <!-- Card Title -->
                <h2 class="text-center font-bold py-8 text-3xl lg:text-4xl text-blue-700 uppercase">
                    Iniciar Sesion
                </h2>
                <FormKit id="loginForm" type="form" :actions="false"
                    incomplete-messages="No se pudo enviar, revisa los datos" @submit="onLogin">

                    <FormKit type="email" label="Corroe Electronico" name="email"
                        placeholder="Ingrese su correo electronico" validation="required|email" :validation-messages="{
                            required: 'El correo electronico es obligatorio',
                            email: 'El nombre es muy corto'
                        }" />

                    <FormKit type="password" label="Contraseña" name="password" placeholder="Ingrese su Contraseña"
                        validation="required|" :validation-messages="{
                            required: 'La contraseña es obligatorio',
                            length: 'La contraseña debe tener al meno 8 caracteres'
                        }" />

                    <FormKit type="submit">iniciar sesion</FormKit>

                </FormKit>

                <!-- Another Auth Routes -->
                <div class="sm:flex sm:flex-wrap mt-8 sm:mb-4 text-sm text-center">
                    <RouterLink to="olvide-password" class="flex-2 underline">
                        Ha olvidado su contraseña
                    </RouterLink>

                    <p class="flex-1 text-gray-500 text-md mx-4 my-1 sm:my-auto">
                        or
                    </p>

                    <RouterLink to="registro" class="flex-2 underline ">
                        Registrate aqui
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


const onLogin = async (formData) => {
    try {
        const { data } = await AuthApi.login(formData);

        localStorage.setItem("access_token", data.data.access_token);

        console.log(data)

        toast(data.message, {
            duration: 3000,
            type: 'success',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
        setTimeout(() => {
            router.push({ name: 'aside' })
        }, 3000);

        reset('loginForm')

    } catch (error) {
        const errorMessage = error.response?.data?.message || "Error al iniciar sesión";
        console.log(errorMessage);


        toast(errorMessage, {
            duration: 3000,
            type: 'error',
            theme: 'colored',
            position: toast.POSITION.TOP_CENTER
        });
    }

}




</script>
