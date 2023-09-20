CodeMirrorComponent = {
    inheritAttrs: false,
    props: ['modelValue', 'mode', 'on_code_mirror_ready'],
    emits: ['update:modelValue'],
    data() {
        return {
            noteCodeMirror: undefined,
        };
    },
    computed: {
        value: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit('update:modelValue', value);
            },
        }
    },
    template: `<div><textarea v-model="value" v-bind="$attrs"></textarea></div>`,
    mounted() {
        this.noteCodeMirror = CodeMirror.fromTextArea(
            this.$el.children[0],
            {
                theme: "default",
                lineNumbers: true,
                mode: this.mode,
                lineWrapping: true,
                extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"},
            },
        );
        let self = this;
        this.noteCodeMirror.getDoc().on(
            'change',
            function(doc) {self.value = doc.getValue();},
        );
        if (this.on_code_mirror_ready) {
            this.on_code_mirror_ready(this.noteCodeMirror);
        }
    },
}
