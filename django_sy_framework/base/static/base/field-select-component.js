FieldSelectComponent = {
    props: ['name', 'modelValue', 'options'],
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
    template: `
        <div class="mb-3 form-group" :id="name + '-group'">
            <div class="form-floating">
                <select class="form-select" :id="name + '-field'" v-model="value" :name="name"  v-bind="$attrs">
                    <option :value="opt_value" v-for="(opt_name, opt_value) of options" :selected="value == opt_name">[[ opt_name ]]</option>
                </select>
                <label :for="name + '-field'" class="form-label"><slot/></label>
            </div>
        </div>
    `,
}
