import {
  CompassIcon,
  GraduationCapIcon,
  ImageIcon,
  MicroscopeIcon,
  PenLineIcon,
  ShapesIcon,
  SparklesIcon,
  VideoIcon,
} from "lucide-react";

import type { Translations } from "./types";

export const koKR: Translations = {
  // Locale meta
  locale: {
    localName: "한국어",
  },

  // Common
  common: {
    home: "홈",
    settings: "설정",
    delete: "삭제",
    rename: "이름 변경",
    share: "공유",
    openInNewWindow: "새 창에서 열기",
    close: "닫기",
    more: "더보기",
    search: "검색",
    download: "다운로드",
    thinking: "생각 중",
    artifacts: "아티팩트",
    public: "공개",
    custom: "사용자 정의",
    notAvailableInDemoMode: "데모 모드에서 사용할 수 없습니다",
    loading: "로딩 중...",
    version: "버전",
    lastUpdated: "마지막 업데이트",
    code: "코드",
    preview: "미리보기",
    cancel: "취소",
    save: "저장",
    install: "설치",
    create: "생성",
  },

  // Welcome
  welcome: {
    greeting: "다시 만나 반갑습니다!",
    description:
      "🦌 DeerFlow에 오신 것을 환영합니다. 오픈 소스 슈퍼 에이전트인 DeerFlow는 내장 및 사용자 정의 스킬을 통해 웹 검색, 데이터 분석, 슬라이드나 웹 페이지 같은 아티팩트 생성 등 거의 모든 작업을 도와드립니다.",

    createYourOwnSkill: "나만의 스킬 만들기",
    createYourOwnSkillDescription:
      "DeerFlow의 강력한 기능을 활용하기 위해 나만의 스킬을 만들어보세요. 사용자 정의 스킬을 통해\nDeerFlow는 웹 검색, 데이터 분석, 슬라이드나 웹 페이지 같은\n 아티팩트 생성 등 거의 모든 작업을 수행할 수 있습니다.",
  },

  // Clipboard
  clipboard: {
    copyToClipboard: "클립보드에 복사",
    copiedToClipboard: "클립보드에 복사되었습니다",
    failedToCopyToClipboard: "클립보드 복사 실패",
    linkCopied: "링크가 클립보드에 복사되었습니다",
  },

  // Input Box
  inputBox: {
    placeholder: "오늘 무엇을 도와드릴까요?",
    createSkillPrompt:
      "`skill-creator`를 사용하여 단계별로 새로운 스킬을 만들어보겠습니다. 먼저, 이 스킬이 어떤 기능을 수행하기를 원하시나요?",
    addAttachments: "첨부파일 추가",
    mode: "모드",
    flashMode: "Flash",
    flashModeDescription: "빠르고 효율적이지만 정확도가 낮을 수 있습니다",
    reasoningMode: "Reasoning",
    reasoningModeDescription:
      "행동하기 전에 추론하여 시간과 정확도의 균형을 맞춥니다",
    proMode: "Pro",
    proModeDescription:
      "추론, 계획 및 실행을 통해 더 정확한 결과를 얻지만, 시간이 더 걸릴 수 있습니다",
    ultraMode: "Ultra",
    ultraModeDescription:
      "작업을 분할하는 서브에이전트가 포함된 Pro 모드; 복잡한 다단계 작업에 최적",
    reasoningEffort: "추론 수준",
    reasoningEffortMinimal: "최소",
    reasoningEffortMinimalDescription: "검색 + 직접 출력",
    reasoningEffortLow: "낮음",
    reasoningEffortLowDescription: "간단한 논리 확인 + 얕은 추론",
    reasoningEffortMedium: "보통",
    reasoningEffortMediumDescription:
      "다층 논리 분석 + 기본 검증",
    reasoningEffortHigh: "높음",
    reasoningEffortHighDescription:
      "전방위 논리 추론 + 다중 경로 검증 + 역방향 확인",
    searchModels: "모델 검색...",
    surpriseMe: "놀라게 해주세요",
    surpriseMePrompt: "놀라게 해주세요",
    followupLoading: "후속 질문 생성 중...",
    followupConfirmTitle: "제안을 보내시겠습니까?",
    followupConfirmDescription:
      "입력란에 이미 텍스트가 있습니다. 전송 방법을 선택하세요.",
    followupConfirmAppend: "추가하여 전송",
    followupConfirmReplace: "교체하여 전송",
    suggestions: [
      {
        suggestion: "작성",
        prompt: "[주제]에 대한 최신 트렌드를 다루는 블로그 글 작성",
        icon: PenLineIcon,
      },
      {
        suggestion: "조사",
        prompt:
          "[주제]에 대한 심층 조사를 수행하고 결과를 요약",
        icon: MicroscopeIcon,
      },
      {
        suggestion: "수집",
        prompt: "[출처]에서 데이터를 수집하고 보고서 작성",
        icon: ShapesIcon,
      },
      {
        suggestion: "학습",
        prompt: "[주제]에 대해 학습하고 튜토리얼 작성",
        icon: GraduationCapIcon,
      },
    ],
    suggestionsCreate: [
      {
        suggestion: "웹페이지",
        prompt: "[주제]에 대한 웹페이지 생성",
        icon: CompassIcon,
      },
      {
        suggestion: "이미지",
        prompt: "[주제]에 대한 이미지 생성",
        icon: ImageIcon,
      },
      {
        suggestion: "동영상",
        prompt: "[주제]에 대한 동영상 생성",
        icon: VideoIcon,
      },
      {
        type: "separator",
      },
      {
        suggestion: "스킬",
        prompt:
          "`skill-creator`를 사용하여 단계별로 새로운 스킬을 만들어보겠습니다. 먼저, 이 스킬이 어떤 기능을 수행하기를 원하시나요?",
        icon: SparklesIcon,
      },
    ],
  },

  // Sidebar
  sidebar: {
    newChat: "새 채팅",
    chats: "채팅",
    recentChats: "최근 채팅",
    demoChats: "데모 채팅",
    agents: "에이전트",
  },

  // Agents
  agents: {
    title: "에이전트",
    description:
      "특화된 프롬프트와 기능을 가진 사용자 정의 에이전트를 생성하고 관리합니다.",
    newAgent: "새 에이전트",
    emptyTitle: "사용자 정의 에이전트가 없습니다",
    emptyDescription:
      "특화된 시스템 프롬프트로 첫 번째 사용자 정의 에이전트를 만들어보세요.",
    chat: "채팅",
    delete: "삭제",
    deleteConfirm:
      "정말로 이 에이전트를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.",
    deleteSuccess: "에이전트가 삭제되었습니다",
    newChat: "새 채팅",
    createPageTitle: "에이전트 디자인",
    createPageSubtitle:
      "원하는 에이전트를 설명해주세요 - 대화를 통해 만들어드리겠습니다.",
    nameStepTitle: "새 에이전트 이름 지정",
    nameStepHint:
      "문자, 숫자, 하이픈만 사용 가능 — 소문자로 저장됩니다 (예: code-reviewer)",
    nameStepPlaceholder: "예: code-reviewer",
    nameStepContinue: "계속",
    nameStepInvalidError:
      "유효하지 않은 이름 — 문자, 숫자, 하이픈만 사용하세요",
    nameStepAlreadyExistsError: "이미 같은 이름의 에이전트가 존재합니다",
    nameStepCheckError: "이름 사용 가능 여부를 확인할 수 없습니다 — 다시 시도해주세요",
    nameStepBootstrapMessage:
      "새 사용자 정의 에이전트 이름은 {name}입니다. **SOUL**을 부트스트랩해봅시다.",
    agentCreated: "에이전트가 생성되었습니다!",
    startChatting: "채팅 시작",
    backToGallery: "갤러리로 돌아가기",
  },

  // Breadcrumb
  breadcrumb: {
    workspace: "작업공간",
    chats: "채팅",
  },

  // Workspace
  workspace: {
    officialWebsite: "DeerFlow 공식 웹사이트",
    githubTooltip: "GitHub의 DeerFlow",
    settingsAndMore: "설정 및 더보기",
    visitGithub: "GitHub의 DeerFlow",
    reportIssue: "이슈 보고",
    contactUs: "문의하기",
    about: "DeerFlow 정보",
  },

  // Conversation
  conversation: {
    noMessages: "메시지가 없습니다",
    startConversation: "대화를 시작하여 여기에 메시지를 표시하세요",
  },

  // Chats
  chats: {
    searchChats: "채팅 검색",
  },

  // Page titles (document title)
  pages: {
    appName: "DeerFlow",
    chats: "채팅",
    newChat: "새 채팅",
    untitled: "제목 없음",
  },

  // Tool calls
  toolCalls: {
    moreSteps: (count: number) => `${count}개의 추가 단계`,
    lessSteps: "단계 줄이기",
    executeCommand: "명령 실행",
    presentFiles: "파일 표시",
    needYourHelp: "도움이 필요합니다",
    useTool: (toolName: string) => `"${toolName}" 도구 사용`,
    searchFor: (query: string) => `"${query}" 검색`,
    searchForRelatedInfo: "관련 정보 검색",
    searchForRelatedImages: "관련 이미지 검색",
    searchForRelatedImagesFor: (query: string) =>
      `"${query}"에 대한 관련 이미지 검색`,
    searchOnWebFor: (query: string) => `웹에서 "${query}" 검색`,
    viewWebPage: "웹 페이지 보기",
    listFolder: "폴더 목록",
    readFile: "파일 읽기",
    writeFile: "파일 쓰기",
    clickToViewContent: "클릭하여 파일 내용 보기",
    writeTodos: "할 일 목록 업데이트",
    skillInstallTooltip: "스킬을 설치하고 DeerFlow에서 사용 가능하게 만들기",
  },

  // Subtasks
  uploads: {
    uploading: "업로드 중...",
    uploadingFiles: "파일 업로드 중입니다. 잠시만 기다려주세요...",
  },

  subtasks: {
    subtask: "하위 작업",
    executing: (count: number) =>
      `${count === 1 ? "" : count + "개의 "}하위 작업${count === 1 ? "" : "을 병렬로"} 실행 중`,
    in_progress: "하위 작업 실행 중",
    completed: "하위 작업 완료",
    failed: "하위 작업 실패",
  },

  // Errors
  errors: {
    streamError: "메시지 스트리밍 중 오류가 발생했습니다. 다시 시도해주세요.",
  },

  // Settings
  settings: {
    title: "설정",
    description: "DeerFlow의 외관과 동작 방식을 조정합니다.",
    sections: {
      appearance: "외관",
      memory: "메모리",
      tools: "도구",
      skills: "스킬",
      notification: "알림",
      about: "정보",
    },
    memory: {
      title: "메모리",
      description:
        "DeerFlow는 백그라운드에서 대화를 통해 자동으로 학습합니다. 이러한 메모리는 DeerFlow가 사용자를 더 잘 이해하고 보다 개인화된 경험을 제공하는 데 도움이 됩니다.",
      empty: "표시할 메모리 데이터가 없습니다.",
      rawJson: "원시 JSON",
      markdown: {
        overview: "개요",
        userContext: "사용자 컨텍스트",
        work: "업무",
        personal: "개인",
        topOfMind: "최우선",
        historyBackground: "히스토리",
        recentMonths: "최근 몇 개월",
        earlierContext: "이전 컨텍스트",
        longTermBackground: "장기 배경",
        updatedAt: "업데이트 시간",
        facts: "사실",
        empty: "(비어 있음)",
        table: {
          category: "카테고리",
          confidence: "신뢰도",
          confidenceLevel: {
            veryHigh: "매우 높음",
            high: "높음",
            normal: "보통",
            unknown: "알 수 없음",
          },
          content: "내용",
          source: "출처",
          createdAt: "생성 시간",
          view: "보기",
        },
      },
    },
    appearance: {
      themeTitle: "테마",
      themeDescription:
        "인터페이스가 기기를 따를지 고정할지 선택하세요.",
      system: "시스템",
      light: "라이트",
      dark: "다크",
      systemDescription: "운영 체제 설정에 자동으로 맞춥니다.",
      lightDescription: "대낮을 위한 높은 대비의 밝은 팔레트입니다.",
      darkDescription: "집중을 위해 눈부심을 줄이는 어두운 팔레트입니다.",
      languageTitle: "언어",
      languageDescription: "언어를 전환합니다.",
    },
    tools: {
      title: "도구",
      description: "MCP 도구의 구성 및 활성화 상태를 관리합니다.",
    },
    skills: {
      title: "에이전트 스킬",
      description:
        "에이전트 스킬의 구성 및 활성화 상태를 관리합니다.",
      createSkill: "스킬 생성",
      emptyTitle: "에이전트 스킬이 없습니다",
      emptyDescription:
        "DeerFlow 루트 폴더 아래 `/skills/custom` 폴더에 에이전트 스킬 폴더를 추가하세요.",
      emptyButton: "첫 번째 스킬 생성하기",
    },
    notification: {
      title: "알림",
      description:
        "DeerFlow는 창이 활성화되지 않았을 때만 완료 알림을 보냅니다. 이는 장시간 실행되는 작업에 특히 유용하므로 다른 작업으로 전환하고 완료되면 알림을 받을 수 있습니다.",
      requestPermission: "알림 권한 요청",
      deniedHint:
        "알림 권한이 거부되었습니다. 브라우저의 사이트 설정에서 활성화하여 완료 알림을 받을 수 있습니다.",
      testButton: "테스트 알림 보내기",
      testTitle: "DeerFlow",
      testBody: "테스트 알림입니다.",
      notSupported: "브라우저가 알림을 지원하지 않습니다.",
      disableNotification: "알림 비활성화",
    },
    acknowledge: {
      emptyTitle: "감사의 말",
      emptyDescription: "크레딧과 감사의 말이 여기에 표시됩니다.",
    },
  },
};
