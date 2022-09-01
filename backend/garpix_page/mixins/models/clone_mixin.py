

class CloneMixin:

    class Meta:
        abstract = True


    def clone_object(self, **args):  # noqa

        related_objects_to_copy = []
        relations_to_set = {}

        for field in self._meta.get_fields():
            if field.one_to_many:
                related_object_manager = getattr(self, field.name, None)
                if not related_object_manager:
                    related_object_manager = getattr(self, f'{field.name}_set')

                related_objects = list(related_object_manager.all())
                if related_objects:
                    related_objects_to_copy += related_objects

            elif field.many_to_many:
                related_object_manager = getattr(self, field.name)
                relations = list(related_object_manager.all())
                if relations:
                    relations_to_set[field.name] = relations

        self.pk = None
        self.id = None

        for key, value in args.items():
            if value:
                setattr(self, key, value)

        self.save()

        for related_object in related_objects_to_copy:
            for related_object_field in related_object._meta.fields:
                if related_object_field.related_model == self.__class__:
                    related_object.pk = None
                    setattr(related_object, related_object_field.name, self)
                    related_object.save()

        for field_name, relations in relations_to_set.items():
            field = getattr(self, field_name)
            field.set(relations)
            text_relations = []
            for relation in relations:
                text_relations.append(str(relation))

        return self
