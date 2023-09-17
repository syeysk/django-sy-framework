MapFieldComponent = {
    props: ['modelValue', 'name', 'map', 'fieldNamePrefix'],
    emits: ['update:modelValue'],
    components: {CodeMirrorComponent},
    data() {
        return {prefixed_name: (this.fieldNamePrefix || 'cred-') + this.name};
    },
    computed: {
        value: {
            get() {
                let values = JSON.parse(this.modelValue);
                let value = values[this.name];
                if (this.map.type == 'object' && value != undefined && value != '') {
                    value = JSON.stringify(value);
                }
                return value ? value.toString() : '';
            },
            set(value) {
                let values = JSON.parse(this.modelValue);
                if (this.map.type == 'object') {
                    value = JSON.parse(value);
                }
                values[this.name] = value;
                this.$emit('update:modelValue', JSON.stringify(values));
            },
        },
    },
    template: `
    <div>
        <div class="mb-3 form-group" :id="prefixed_name + '-group'" v-if="map.type=='string' && map.enum">
            <div class="form-floating">
                <select v-model="value" v-bind="$attrs" class="form-select form-select-lg mb-3" :id="prefixed_name + '-field'" :name="prefixed_name">
                    <option
                        v-for="variant in map.enum"
                        :value="variant"
                        :selected="value != value"
                    >[[ variant ]]</option>
                </select>
                <label :for="prefixed_name + '-field'" class="form-label">[[ map.description ]]</label>
            </div>
        </div>
        <div class="mb-3 form-group" :id="prefixed_name + '-group'" v-else-if="map.type=='string'">
            <div class="form-floating">
                <input v-model="value" v-bind="$attrs" class="form-control" type="text" :id="prefixed_name + '-field'" :pattern="map.pattern" :name="prefixed_name">
                <label :for="prefixed_name + '-field'" class="form-label">[[ map.description ]]</label>
            </div>
        </div>
        <div class="mb-3 form-group" :id="prefixed_name + '-group'" v-else-if="map.type=='integer'">
            <div class="form-floating">
                <input v-model="value" v-bind="$attrs" class="form-control" type="number" :id="prefixed_name + '-field'" :name="prefixed_name">
                <label :for="prefixed_name + '-field'" class="form-label">[[ map.description ]]</label>
            </div>
        </div>
        <div class="form-group" :id="prefixed_name + '-group'" v-else-if="map.type=='object'">
            <label :for="prefixed_name + '-field'">[[ map.description ]]</label>
            <code-mirror-component
                v-model="value"
                v-bind="$attrs"
                class="form-control"
                :id="prefixed_name + '-field'"
                mode="application/ld+json"
                :name="prefixed_name"
            ></code-mirror-component>
        </div>
    </div>
    `,
}
