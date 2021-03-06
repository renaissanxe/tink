# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tink.tools.testing.cross_language.util.cli_daead."""

from absl.testing import absltest
from absl.testing import parameterized

import tink
from tink import daead

from tools.testing.cross_language.util import cli_daead


def setUpModule():
  daead.register()


class CliDaeadTest(parameterized.TestCase):

  @parameterized.parameters(*cli_daead.LANGUAGES)
  def test_encrypt_decrypt_success(self, lang):
    keyset_handle = tink.new_keyset_handle(
        daead.deterministic_aead_key_templates.AES256_SIV)
    p = cli_daead.CliDeterministicAead(lang, keyset_handle)
    plaintext = b'plaintext'
    associated_data = b'associated_data'
    ciphertext = p.encrypt_deterministically(plaintext, associated_data)
    output = p.decrypt_deterministically(ciphertext, associated_data)
    self.assertEqual(output, plaintext)

  @parameterized.parameters(*cli_daead.LANGUAGES)
  def test_invalid_decrypt_raises_error(self, lang):
    keyset_handle = tink.new_keyset_handle(
        daead.deterministic_aead_key_templates.AES256_SIV)
    p = cli_daead.CliDeterministicAead(lang, keyset_handle)
    with self.assertRaises(tink.TinkError):
      p.decrypt_deterministically(b'invalid ciphertext', b'associated_data')


if __name__ == '__main__':
  absltest.main()
