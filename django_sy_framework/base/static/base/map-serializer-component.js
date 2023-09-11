MapSerializerComponent = {
    props: ['serializerMap', 'modelValue', 'useDefaultValue'],
    emits: ['update:modelValue'],
    computed: {
        value: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit('update:modelValue', value);
            },
        },
    },
    data() {
        return {mUseDefaultValue: this.useDefaultValue};
    },
    components: {MapFieldComponent},
    template: `
        <map-field-component
            v-for="field in serializerMap"
            :key="field.name"
            :name="field.name"
            :map="field.map"
            v-model="value"
        ></map-field-component>
        <input type="hidden" v-model="value" v-bind="$attrs">
    `,
}
