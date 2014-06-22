from django.test import TestCase
from django.utils import translation
from misago.core import migrationutils
from misago.core.models import CacheVersion


class LazyTranslationStringTests(TestCase):
    def setUp(self):
        translation.activate('de')

    def tearDown(self):
        translation.deactivate()

    def test_ugettext_lazy(self):
        """ugettext_lazy for migrations maintains untranslated message"""
        string = migrationutils.ugettext_lazy('content type')
        self.assertEqual(string.message, 'content type')
        self.assertEqual(unicode(string), 'Inhaltstyp')


class OriginalMessageTests(TestCase):
    def test_original_message(self):
        """original_message returns untranslated message for misago messages"""
        string = migrationutils.ugettext_lazy('content type')

        self.assertEqual(migrationutils.original_message(string),
                         string.message)
        self.assertEqual("Lorem ipsum", "Lorem ipsum")


class CacheBusterUtilsTests(TestCase):
    def setUp(self):
        self.orm = {
            'core.CacheVersion': CacheVersion,
        }

    def test_with_core_models(self):
        """with_core_models builds correct dict of models"""
        models = {
            u'conf.setting': {
                'Meta': {'object_name': 'Setting'},
                'default_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                'dry_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                'form_field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': u"text"}),
                'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conf.SettingsGroup']"}),
                u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
                'is_lazy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
                'legend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
                'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
                'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
                'pickled_field_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                'python_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': u"string"}),
                'setting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
            },
            u'conf.settingsgroup': {
                'Meta': {'object_name': 'SettingsGroup'},
                'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
                'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
                'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
            }
        }

        final_models = migrationutils.with_core_models('0001_initial')
        self.assertTrue('core.cacheversion' in final_models),

        final_models = migrationutils.with_core_models('0001_initial', models)
        self.assertTrue('core.cacheversion' in final_models),
        self.assertTrue('conf.settingsgroup' in final_models),
        self.assertTrue('conf.setting' in final_models),

    def test_cachebuster_register_cache(self):
        """
        cachebuster_register_cache registers cache on migration successfully
        """

        cache_name = 'eric_licenses'
        migrationutils.cachebuster_register_cache(self.orm, cache_name)
        CacheVersion.objects.get(cache=cache_name)

    def test_cachebuster_unregister_cache(self):
        """
        cachebuster_unregister_cache removes cache on migration successfully
        """

        cache_name = 'eric_licenses'
        migrationutils.cachebuster_register_cache(self.orm, cache_name)
        CacheVersion.objects.get(cache=cache_name)

        migrationutils.cachebuster_unregister_cache(self.orm, cache_name)
        with self.assertRaises(CacheVersion.DoesNotExist):
            CacheVersion.objects.get(cache=cache_name)

        with self.assertRaises(ValueError):
            migrationutils.cachebuster_unregister_cache(self.orm, cache_name)
