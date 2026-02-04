#!/usr/bin/env python3

#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse

from google.cloud import storage

from results_uploader import results_uploader


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Parses the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gcs_dir',
        required=True,
        help='Directory to save test artifacts in GCS.',
    )
    parser.add_argument(
        '--gcs_bucket',
        help='Bucket in GCS where test artifacts are uploaded. If unspecified, '
             'use the current GCP project name as the bucket name.',
    )


def _download_gcs_dir(gcs_bucket: str, gcs_dir: str, dest_dir: pathlib.Path):
    """
    Downloads a directory from GCS to a local directory.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)

    # Ensure gcs_dir ends with a slash if it's not empty, to use as a prefix filter
    if gcs_dir and not gcs_dir.endswith('/'):
        gcs_dir += '/'

    # List all blobs with the specified prefix (simulates listing directory contents)
    blobs = bucket.list_blobs(prefix=gcs_dir)

    for blob in blobs:
        # Skip blobs that might just be the directory placeholder itself (if present)
        if blob.name.endswith('/'):
            continue

        # Determine the full local file path
        # If gcs_dir is provided, we remove it from the blob name to map to dest_dir
        relative_path = os.path.relpath(blob.name,
                                        gcs_dir) if gcs_dir else blob.name
        destination_file_path = os.path.join(dest_dir, relative_path)

        # Create local parent directories if they don't exist
        Path(os.path.dirname(destination_file_path)).mkdir(parents=True,
                                                           exist_ok=True)

        # Download the file
        print(f"Downloading {blob.name} to {destination_file_path}")
        blob.download_to_filename(destination_file_path)


def main(argv: list[str] | None = None) -> None:
    """
    Using Mobly logs already uploaded to GCS, process the results and
    upload to Resultstore.
    """
    args = _parse_args(argv)

    # Download the Mobly logs from GCS directory
    tmp_mobly_dir = None

    # Run the local results_uploader, skipping the GCS upload of the Mobly logs
    results_uploader.main(
        [tmp_mobly_dir, '--use_existing_gcs_mobly_logs', *argv]
    )


if __name__ == '__main__':
    main()
