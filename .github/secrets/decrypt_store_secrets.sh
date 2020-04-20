#!/bin/sh

gpg --quiet --batch --yes --decrypt --passphrase="$IOS_PROFILE_KEY" --output .github/secrets/storeprofile.mobileprovision .github/secrets/storeprofile.mobileprovision.gpg
gpg --quiet --batch --yes --decrypt --passphrase="$IOS_PROFILE_KEY" --output .github/secrets/Certificates.p12 .github/secrets/Certificates.p12.gpg



mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles

cp .github/secrets/storeprofile.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/b1acf2fb-b685-4ba4-8a7c-55b9f26d9cdc.mobileprovision


security create-keychain -p "" build.keychain
security import .github/secrets/Certificates.p12 -t agg -k ~/Library/Keychains/build.keychain -P "" -A

security set-keychain-settings -t 3600 -l ~/Library/Keychains/build.keychain
security list-keychains -s ~/Library/Keychains/build.keychain
security default-keychain -s ~/Library/Keychains/build.keychain
security unlock-keychain -p "" ~/Library/Keychains/build.keychain


security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "" ~/Library/Keychains/build.keychain
