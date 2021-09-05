<template>
    <div>
        <div class="close-form" v-on:click="close_form">
                <img src="../assets/images_header/close-icon.svg" height="30">
            </div>
        <div class="identification__form">
            <div class="identification__manage">
                <h3 v-on:click="identification_count = 2; identificationTabClick()" v-bind:class="{ activeIdentification: identification_count == 2}">Вход</h3>
                <h3 v-on:click="identification_count = 1; identificationTabClick()" v-bind:class="{ activeIdentification: identification_count == 1}">Регистрация</h3>
            </div>
            <div class="identification__change" v-show="identification_count == 1">
                <div class="radioButtons">
                    <div class="radioButton">
                        <input class="custom-radio" name="color" type="radio" id="provider" value="provider" v-model="client">
                        <label for="provider">Вы поставщик</label>
                    </div>
                    <div class="radioButton">
                        <input class="custom-radio" name="color" type="radio" id="customer" value="customer" v-model="client">
                        <label for="customer">Вы покупатель</label>
                    </div>
                </div>
            </div>
            <div class="identification__inputs">
                    <div class="identification__input" v-show="identification_count == 1 && client == 'customer'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="name_reg != ''" v-on:click="name_reg = ''">
                        <div>
                            <p>Имя*</p>
                            <span class="input__error-text" v-if="input_reg_error_text_name != ''">✖ {{ input_reg_error_text_name }}</span>
                        </div>
                        <input type="text" placeholder="Анастасия" v-model="name_reg" v-bind:class="{ input__error: name_reg_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'customer'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="lastname_reg != ''" v-on:click="lastname_reg = ''">
                        <div>
                            <p>Фамилия*</p>
                            <span class="input__error-text" v-if="input_reg_error_text_lastname != ''">✖ {{ input_reg_error_text_lastname }}</span>
                        </div>
                        <input type="text" placeholder="Скоморохова" v-model="lastname_reg" v-bind:class="{ input__error: lastname_reg_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'customer'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="email_reg != ''" v-on:click="email_reg = ''">
                        <div>
                            <p>Почта*</p>
                            <span class="input__error-text" v-if="input_reg_error_text_email != ''">✖ {{ input_reg_error_text_email }}</span>
                        </div>
                        <input type="text" placeholder="mail@gmail.com" v-model="email_reg" v-bind:class="{ input__error: email_reg_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'customer'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="phone_reg != ''" v-on:click="phone_reg = ''">
                        <div>
                            <p>Номер телефона</p>
                            <span class="input__error-text" v-if="input_reg_error_text_phone != ''">✖ {{ input_reg_error_text_phone }}</span>
                        </div>
                        <masked-input mask="\+1\ (111) 111-11-11" placeholder="+7 (900) 990-90-99" v-model="phone_reg" v-bind:class="{ input__error: phone_reg_error == true }"/>
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'customer'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="password_reg != ''" v-on:click="password_reg = ''">
                        <div>
                            <p>Пароль*</p>
                            <span class="input__error-text" v-if="input_reg_error_text_password != ''">✖ {{ input_reg_error_text_password }}</span>
                        </div>
                        <input type="password" placeholder="***********" v-model="password_reg" v-bind:class="{ input__error: password_reg_error == true }">
                    </div>
                    <!--Для поставщика-->
                    <div class="identification__input" v-show="identification_count == 1 && client == 'provider'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="name_company != ''" v-on:click="name_company = ''">
                        <div>
                            <p>Название компании*</p>
                            <span class="input__error-text" v-if="name_company_error_text != ''">✖ {{ name_company_error_text }}</span>
                        </div>
                        <input type="text" placeholder="ООО «Обувной»" v-model="name_company" v-bind:class="{ input__error: name_company_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'provider'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="description_company != ''" v-on:click="description_company = ''">
                        <div>
                            <p>Описание компании*</p>
                            <span class="input__error-text" v-if="description_company_error_text != ''">✖ {{ description_company_error_text }}</span>
                        </div>
                        <input type="text" placeholder="ООО «Обувной» занимается поставкой обуви более 10 лет." v-model="description_company" v-bind:class="{ input__error: description_company_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'provider'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="email_company != ''" v-on:click="email_company = ''">
                        <div>
                            <p>Почта*</p>
                            <span class="input__error-text" v-if="email_company_error_text != ''">✖ {{ email_company_error_text }}</span>
                        </div>
                        <input type="text" placeholder="mail@gmail.com" v-model="email_company" v-bind:class="{ input__error: email_company_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 1 && client == 'provider'">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="password_company != ''" v-on:click="password_company = ''">
                        <div>
                            <p>Пароль*</p>
                            <span class="input__error-text" v-if="password_company_error_text != ''">✖ {{ password_company_error_text }}</span>
                        </div>
                        <input type="password" placeholder="***********" v-model="password_company" v-bind:class="{ input__error: password_company_error == true }">
                    </div>
                    <!---->
                    <div class="identification__input" v-show="identification_count == 2">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="email_auth != ''" v-on:click="email_auth = ''">
                        <div>
                            <p>Почта</p>
                            <span class="input__error-text" v-if="input_auth_error_text_email != ''">✖ {{ input_auth_error_text_email }}</span>
                        </div>
                        <input type="text" placeholder="mail@gmail.com" v-model="email_auth" v-bind:class="{ input__error: email_auth_error == true }">
                    </div>
                    <div class="identification__input" v-show="identification_count == 2">
                        <img src="../assets/images_identification/close-icon.svg" class="input__close-icon" v-if="password_auth != ''" v-on:click="password_auth = ''">
                        <div>
                            <p>Пароль</p>
                            <span class="input__error-text" v-if="input_auth_error_text_password != ''">✖ {{ input_auth_error_text_password }}</span>
                        </div>
                        <input type="password" placeholder="***********" v-model="password_auth" v-bind:class="{ input__error: password_auth_error == true }">
                    </div>
            </div>
            <div class="identification__button" v-if="identification_count == 1" v-on:click="registration">
                <h4>Зарегистрироваться</h4>
            </div>
            <div class="identification__button" v-if="identification_count == 2" v-on:click="authorization">
                <h4>Вход</h4>
            </div>
            <p class="registration__text-1" v-if="identification_count == 1">*Обязательные поля для заполнения</p>
            <p class="registration__text-2" v-if="identification_count == 1">Нажимая «Зарегистрироваться» Вы подтверждаете, что ознакомлены, согласны и принимаете условия <span>Пользовательского соглашения</span> и <span>Политики конфиденциальности</span></p>
            <p class="registration__text-2" v-if="identification_count == 2">Не можете войти в систему?<br><span>Обратитесь в службу поддержки!</span></p>
        </div>
    </div>
</template>
<script>
    import maskedInput from 'vue-masked-input';
    import axios from 'axios';
    import { bus } from '../main';
    export default {
        props: ['showAuthorizationProps', 'showRegistrationProps'],
        data() {
            return {
                identification_count: 1,
                name_reg: '',
                lastname_reg: '',
                email_reg: '',
                phone_reg: '',
                password_reg: '',
                email_auth: '',
                password_auth: '',
                name_reg_error: false,
                lastname_reg_error: false,
                email_reg_error: false,
                phone_reg_error: false,
                password_reg_error: false,
                email_auth_error: false,
                password_auth_error: false,
                input_auth_error_text_email: '',
                input_auth_error_text_password: '',
                input_reg_error_text_name: '',
                input_reg_error_text_lastname: '',
                input_reg_error_text_email: '',
                input_reg_error_text_phone: '',
                input_reg_error_text_password: '',
                client: '',
                name_company: '',
                description_company: '',
                email_company: '',
                password_company: '',
                name_company_error: false,
                description_company_error: false,
                email_company_error: false,
                password_company_error: false,
                name_company_error_text: '',
                description_company_error_text: '',
                email_company_error_text: '',
                password_company_error_text: '',
                local_success: ''
            }
        },
        components: {
            maskedInput
        },
        created() {
            this.client = 'customer';
            if(this.showAuthorizationProps == true) {
                this.identification_count = 2
            }
            if(this.showRegistrationProps == true) {
                this.identification_count = 1
            }
        },
        methods: {
            identificationTabClick() {
                this.error_text = ''
            },
            close_form() {
                console.log('close form вызвалась')
                bus.$emit('closeIdentificationFormHeader', false);
                this.$emit('closeIdentificationForm', {
                    statusIdentificationForm: false
                })
            },
            registration() {
                if(this.client == 'customer') {
                    this.name_reg_error = false;
                    this.lastname_reg_error = false;
                    this.email_reg_error = false;
                    this.phone_reg_error = false;
                    this.password_reg_error = false;
                    this.input_reg_error_text_name = '';
                    this.input_reg_error_text_lastname = '';
                    this.input_reg_error_text_email = '';
                    this.input_reg_error_text_phone = '';
                    this.input_reg_error_text_password = '';
                    if(this.name_reg == '') {this.name_reg_error = true; this.input_reg_error_text_name = 'Поле пусто.';}
                    if(this.lastname_reg == '') {this.lastname_reg_error = true; this.input_reg_error_text_lastname = 'Поле пусто.';}
                    if(this.email_reg == '') {this.email_reg_error = true; this.input_reg_error_text_email = 'Поле пусто.';}
                    if(this.password_reg == '') {this.password_reg_error = true;  this.input_reg_error_text_password = 'Поле пусто.';}
                    if (!(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.email_reg))) {
                        this.email_reg_error = true;
                        this.input_reg_error_text_email = 'Почта некорректна.';
                    }
                    if(this.phone_reg != '' && parseInt(this.phone_reg.replace(/\D+/g,"")).toString().length != 11) {
                        this.phone_reg_error = true;
                        this.input_reg_error_text_phone = 'Номер некорректен.';
                    }
                    if(this.name_reg_error == false && this.lastname_reg_error == false && this.email_reg_error == false && this.phone_reg_error == false && this.password_reg_error == false) {
                        axios
                            .post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                                module: 'sign_up_customer',
                                first_name: this.name_reg,
                                last_name: this.lastname_reg,
                                email: this.email_reg,
                                phone: this.phone_reg,
                                password: this.password_reg
                            })
                            .then(response => {
                                console.log(response)
                                if(response.data.status == true) {
                                    this.local_success = true;
                                    bus.$emit('checkAuthNow', this.local_success);
                                    bus.$emit('closeIdentificationFormHeader', false);
                                    this.$emit('closeIdentificationForm', {
                                        statusIdentificationForm: false
                                    })
                                    this.$emit('showModal', {
                                        show_modal_status: true
                                    });
                                    this.$emit('emailCorrect', {
                                        email_correct_status: response.data.mail_send,
                                        email_clean: this.email_reg
                                    });
                                }
                            })
                            .catch(error => {
                                console.log(error)
                            })
                    }
                } else if(this.client == 'provider') {
                    this.name_company_error = false;
                    this.description_company_error = false;
                    this.email_company_error = false;
                    this.password_company_error = false;
                    this.name_company_error_text = '';
                    this.description_company_error_text = '';
                    this.email_company_error_text = '';
                    this.password_company_error_text = '';
                    if(this.name_company == '') {this.name_company_error = true; this.name_company_error_text = 'Поле пусто.';}
                    if(this.description_company == '') {this.description_company_error = true; this.description_company_error_text = 'Поле пусто.';}
                    if(this.email_company == '') {this.email_company_error = true; this.email_company_error_text = 'Поле пусто.';}
                    if(this.password_company == '') {this.password_company_error = true; this.password_company_error_text = 'Поле пусто.';}
                    if (!(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.email_company))) {
                        this.email_company_error = true;
                        this.email_company_error_text = 'Почта некорректна.';
                    }
                    if(this.name_company_error == false && this.description_company_error == false && this.email_company_error == false && this.password_company_error == false) {
                        axios
                        .post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                            module: 'sign_up_vendor',
                            company_name: this.name_company,
                            description: this.description_company,
                            email: this.email_company,
                            password: this.password_company
                        })
                        .then(response => {
                            console.log(response)
                            if(response.data.status == true) {
                                this.local_success = true;
                                bus.$emit('checkAuthNow', this.local_success);
                                bus.$emit('closeIdentificationFormHeader', false);
                                this.$emit('closeIdentificationForm', {
                                    statusIdentificationForm: false
                                })
                                this.$emit('showModal', {
                                    show_modal_status: true
                                });
                                this.$emit('emailCorrect', {
                                    email_correct_status: response.data.mail_send,
                                    email_clean: this.email_reg
                                });
                            }
                        })
                    }
                }
            },
            authorization() {
                this.input_auth_error_text_email = '';
                this.input_auth_error_text_password = '';
                this.email_auth_error = false;
                this.password_auth_error = false;
                if(this.email_auth == '') {this.email_auth_error = true; this.input_auth_error_text_email = 'Поле пусто.';}
                if(this.password_auth == '') {this.password_auth_error = true; this.input_auth_error_text_password = 'Поле пусто.';}
                if(this.email_auth != '' && this.password_auth != '') {
                    axios
                    .post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                        module: 'sign_in',
                        email: this.email_auth,
                        password: this.password_auth
                    })
                    .then(response => {
                        console.log(response)
                        if(response.data.status == true) {
                            this.local_success = true;
                            bus.$emit('checkAuthNow', this.local_success);
                           bus.$emit('closeIdentificationFormHeader', false);
                            this.$emit('closeIdentificationForm', {
                                statusIdentificationForm: false
                            })
                        }
                    })
                }
            }
        }
    }
</script>
<style scoped lang="scss">
.close-form {
    position: absolute;
    z-index: 10;
    top: 2%;
    right: 5%;
    cursor: pointer;
}
.custom-radio {
    position: absolute;
    z-index: -1;
    opacity: 0;
  }
  
    .custom-radio+label {
    display: inline-flex;
    align-items: center;
    user-select: none;
  }
  
    .custom-radio+label::before {
    content: '';
    display: inline-block;
    width: 1em;
    height: 1em;
    flex-shrink: 0;
    flex-grow: 0;
    border: 1px solid #adb5bd;
    border-radius: 50%;
    margin-right: 0.5em;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 50% 50%;
  }
  .custom-radio:not(:disabled):not(:checked)+label:hover::before {
    border-color: #8f6cc9;
    transition: all 0.1s linear;
  }
  .custom-radio:checked+label::before {
    border-color: #8F6CC9;
    background-color: #8F6CC9;
  }
    .identification {
        font-family: 'Proxima Nova Rg';
        &__change {
                .radioButtons {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 15px;
                    .radioButton {
                        label {
                            font-weight: 600;
                            font-size: 16px;
                            color: #6E7191;
                        }
                    }
                }
            }
        &__form {
            position: relative;
            z-index: 2;
            padding: 64px 64px;

            width: 450px;
            height: 100%;
            background-color: white;
            box-shadow: 0px 2px 18px rgba(143, 108, 201, 0.1);
            border-radius: 16px;

            .identification__button {
                cursor: pointer;
                margin-top: 24px;
                h4 {
                    text-align: center;
                    font-weight: 600;
                    font-size: 18px;
                    color: white;
                    background: #8F6CC9;
                    border-radius: 21px;
                    padding: 8px 74px;
                    display: block;
                }
            }
            .identification__button:hover {
                h4 {
                    background: #7553ad;
                    transition: all 0.1s linear;
                }
            }
        }
        &__manage {
            color: rgba(143, 108, 201, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 21px;

            .activeIdentification {
                color: #8F6CC9 !important;
            }

            h3 {
                cursor: pointer;
                font-weight: bold;
                font-size: 32px;
            }
        }
        &__input {
            margin-top: 16px;
            position: relative;
            .input__close-icon {
                position: absolute;
                top: 50%;
                transform: translate(0, -40%);
                right: 9%;
                display: block;
                cursor: pointer;
            }
            p {
                position: absolute;
                font-weight: 600;
                font-size: 14px;
                color: #8f93c2;
                left: 20.5%;
                top: 18%;
            }
            span.input__error-text {
                color: #d4576c !important;
                position: absolute !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                right: 3% !important;
                top: 1% !important;
            }
            input, masked-input {
                font-weight: normal;
                font-size: 16px;
                color: black;

                z-index: 1;
                -webkit-appearance: none;
                border: 0;
                width: 322px;
                height: 64px;
                border: 2px solid #D9DBE9;
                border-radius: 16px;
                padding-left: 64px;
                padding-right: 64px;
                padding-top: 28px;
            }
            .input__error {
                border: 2px solid #d4576c !important;
                box-shadow: 0px 2px 5px #d4576c !important;
            }
            input::placeholder {
                font-weight: normal;
                font-size: 16px;
                color: #AFB1C3;
            }
            &:first-child input{
                background: url(../assets/images_identification/human-icon.svg) no-repeat 18px 50%, #FCFCFC;
                margin-top: 0;
            }
            &:nth-child(2) input{
                background: url(../assets/images_identification/human-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(3) input{
                background: url(../assets/images_identification/letter-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(4) input{
                background: url(../assets/images_identification/phone-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(5) input{
                background: url(../assets/images_identification/eye-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(6) input{
                background: url(../assets/images_identification/human-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(7) input{
                background: url(../assets/images_identification/file-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(8) input{
                background: url(../assets/images_identification/letter-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(9) input{
                background: url(../assets/images_identification/eye-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(10) input{
                background: url(../assets/images_identification/letter-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
            &:nth-child(11) input{
                background: url(../assets/images_identification/eye-icon.svg) no-repeat 18px 50%, #FCFCFC;
            }
        }
    }
    .registration__text-1 {
        font-weight: normal;
        font-size: 12px;
        color: #222222;
        margin-top: 8px;
    }
    .registration__text-2 {
        margin-top: 16px;
        font-weight: normal;
        font-size: 12px;
        color: #222222;
        text-align: center;

        span {
            cursor: pointer;
            color: #8f6cc9;
            text-decoration: underline;
        }
    }
</style>