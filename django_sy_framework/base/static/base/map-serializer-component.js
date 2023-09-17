MapSerializerComponent = {
    props: ['serializerMap', 'modelValue', 'useDefaultValue', 'fieldNamePrefix'],
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
            v-for="(field_map, field_name) in serializerMap"
            :key="field_name"
            :name="field_name"
            :map="field_map"
            v-model="value"
            :field-name-prefix="fieldNamePrefix"
        ></map-field-component>
        <input type="hidden" v-model="value" v-bind="$attrs">
    `,
}
