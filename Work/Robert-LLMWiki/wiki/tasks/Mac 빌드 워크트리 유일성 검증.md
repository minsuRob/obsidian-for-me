---
유형: 일감
상태: 진행중
우선순위: 중간
생성일: 2026-07-03
갱신일: 2026-07-03
출처:
  - "[[2026-07-03]]"
---

# Mac 빌드 워크트리 유일성 검증

## 배경
`staging-deploy.yml`이 M5 Max Mac을 원격 SSH로 많이 사용한다. **런마다 유일성이 지켜지는지, 중간에 트리가 변경되지 않는지**를 여러 각도로 검증한다.

- 대상: `.github/workflows/staging-deploy.yml`
- 원격 스크립트: `scripts/run-frontend-validate-remote.sh`, `scripts/run-electron-mac-release-remote.sh`, `scripts/run-ios-release-remote.sh`, `scripts/lib/tailscale-ssh-host.sh`

## 현황 — 검증 결과

### ✅ 잘 지켜지는 것
1. **파이프라인 단일성**: `concurrency: staging-deploy` + `cancel-in-progress: true` → staging-deploy는 한 번에 하나, 새 push가 진행중을 취소.
2. **네트워크 유일성**: Tailscale 호스트명 `...-${github.run_id}` (frontend/electron/ios 모두 런별 유일).
3. **빌드 대상 고정(중간변경 방지의 핵심)**: 모든 원격 빌드가 `git reset --hard $GITHUB_SHA` + `git submodule update --init --recursive`로 **트리거 커밋에 고정**. "최신 develop"이 아니라 그 SHA를 빌드 → 중간에 develop이 바뀌어도 빌드물은 불변.
4. **Electron/iOS 릴리스 격리**: 런별 유일 워크트리 `run-${RUN_ID}-${ATTEMPT}-${SHA:0:12}` (경로: `../maki-electron-worktrees`, `../maki-ios-worktrees`), 끝나면 `worktree remove --force`. 종류별 분리 락(`/tmp/maki-electron-release.lock`, `/tmp/maki-ios-release.lock`) + PID 기반 stale 락 자동 정리 → electron·ios는 병렬(최대 2), 같은 종류끼리는 직렬.

### ⚠️ 확인/보완 필요한 위험
1. **Frontend validate = 공유 고정 워크트리 + 무락**
   - 경로가 런별이 아님: `~/.maki-ci-worktrees/frontend-validate` **재사용**, 매 런 `git reset --hard`. **락이 없다.**
   - 위험: 원격 frontend 빌드는 detached가 아니라 SSH 동기 실행(`continue-on-error`). `cancel-in-progress`로 GHA 잡이 취소되면 SSH는 끊기지만 **Mac 위 빌드 프로세스가 살아있을 수 있음**. 다음 런이 같은 공유 워크트리에서 `git reset --hard`를 돌리면 **경쟁/중간변경** 가능. → frontend에도 락 도입 또는 런별 워크트리 검토.
2. **base repo 동시 접근**: frontend 빌드가 base repo에서 `git fetch` + `git worktree prune` + `rm -rf $CI_WORKTREE`. 살아있는 detached electron/iOS 워크트리가 base `.git`을 공유 → 이론상 prune은 사라진 워크트리만 정리하므로 안전하지만, **동시 시점 검증 권장**.
3. **고아 워크트리 누적**: detached 빌드가 강제 종료되면 `maki-electron-worktrees/`·`maki-ios-worktrees/` 하위 디렉토리가 잔존 가능 → 디스크 증가. 주기적 `git worktree prune` + 고아 정리 필요.
4. **index.lock 잔존**: frontend 공유 워크트리는 존재하면 재생성 안 하고 `reset --hard`만 함. 강제 종료로 `.git/worktrees/frontend-validate/index.lock`이 남으면 다음 `reset` 실패 가능. → 사전 `rm -f index.lock` 가드 검토.

## 검증 방법 (다음 액션 — 결정 ✅ 2026-07-03: 지금은 위키 기록만, 실측/코드변경 보류)
- Mac에서 `git worktree list --porcelain`로 현재 워크트리/고아 확인.
- 취소된 frontend 빌드가 remote 프로세스를 실제로 죽이는지 실험(빌드 중 취소 → `pgrep` 확인).
- frontend 빌드에 락(mkdir/flock) 또는 런별 워크트리(`run-${run_id}` 방식) 도입 PoC.

## 타임라인
- 2026-07-03: 워크플로 + 3개 원격 스크립트 정독. electron/ios는 런별 워크트리+락으로 견고, frontend는 공유 워크트리+무락 위험 식별 (출처: [[2026-07-03]]).

## 관련
- [[Electron 버전 통일]]
