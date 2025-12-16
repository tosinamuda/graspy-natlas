import { env } from "@/env.client";
import { auth } from "./firebase";

const API_URL = env.NEXT_PUBLIC_API_URL + "/api";

export async function fetchSubjects(featured: boolean = false) {
  const res = await fetch(`${API_URL}/subjects?featured=${featured}`);
  if (!res.ok) throw new Error("Failed to fetch subjects");
  const data = await res.json();
  return data.subjects;
}

export async function fetchSubjectBySlug(slug: string) {
  const res = await fetch(`${API_URL}/subjects/${slug}`);
  if (!res.ok) return null;
  if (!res.ok) return null;
  return await res.json();
}

export async function fetchTopic(id: string, language: string = "english") {
  const res = await fetch(`${API_URL}/study/topics/${id}?language=${language}`);
  if (!res.ok) return null;
  return await res.json();
}

export async function createTopic(
  subjectId: string,
  title: string,
  context?: string,
  language: string = "english"
) {
  const token = await auth.currentUser?.getIdToken();
  if (!token) throw new Error("Authentication required");

  const res = await fetch(`${API_URL}/study/topics`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ subject_id: subjectId, title, context, language }),
  });

  if (!res.ok) throw new Error("Failed to create topic");
  return await res.json();
}

export async function explainTopic(
  subjectId: string,
  topicTitle: string,
  language: string,
  context?: string
) {
  const token = await auth.currentUser?.getIdToken();
  if (!token) throw new Error("Authentication required");

  const res = await fetch(`${API_URL}/study/explain`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      subject_id: subjectId,
      topic: topicTitle,
      language,
      context,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to explain topic: ${err}`);
  }
  return await res.json();
}

export async function sendChatMessage(
  sessionId: string,
  message: string,
  language: string
) {
  const token = await auth.currentUser?.getIdToken();
  if (!token) throw new Error("Authentication required");

  const res = await fetch(`${API_URL}/study/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ session_id: sessionId, message, language }),
  });

  if (!res.ok) throw new Error("Failed to send message");
  return await res.json();
}

export async function startChatSession(
  topicId: string,
  topicName?: string,
  initialContext?: string
) {
  if (!auth.currentUser) {
    throw new Error("Must be logged in to start chat");
  }

  const token = await auth.currentUser.getIdToken();
  const res = await fetch(`${API_URL}/study/chat/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      topic_id: topicId,
      topic_name: topicName,
      initial_context: initialContext,
    }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Failed to start chat session");
  }

  return res.json();
}

export async function verifyAccessCode(code: string) {
  const token = await auth.currentUser?.getIdToken();
  if (!token)
    return await fetch(`${API_URL}/access/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    }).then((res) => res.json());

  // If logged in, activate account
  const res = await fetch(`${API_URL}/access/activate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) throw new Error("Invalid code");
  return await res.json();
}

export async function getAccessStatus() {
  const token = await auth.currentUser?.getIdToken();
  if (!token) return { is_verified: false };

  const res = await fetch(`${API_URL}/access/status`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) return { is_verified: false };
  return await res.json();
}
